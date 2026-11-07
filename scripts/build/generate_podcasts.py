"""Generate short two-host audio episodes for Hugo posts and project pages.

Two stages, both incremental:

1. ``--scripts``: write ``podcast.<lang>.json`` next to each ``index[.fr].md``.
   Missing scripts are written by Claude through the Messages API
   (needs ``ANTHROPIC_API_KEY``). Style rules live in ``podcast_prompt.md``.
   ``--refresh-stale`` also rewrites scripts whose source page changed.
2. ``--audio``: turn each script into ``podcast.<lang>.mp3`` with edge-tts
   neural voices and ffmpeg (mono, 48 kbit/s, loudness-normalised). Audio is
   only rebuilt when the script lines or voices change.

The Hugo partial ``podcast-player.html`` shows a player when the MP3 exists.

Examples::

    python scripts/build/generate_podcasts.py --scripts --audio
    python scripts/build/generate_podcasts.py --audio --only uml-mcp
    python scripts/build/generate_podcasts.py --check
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "hugo" / "content"
PROMPT = Path(__file__).resolve().parent / "podcast_prompt.md"

LANGS = {"en": "index.md", "fr": "index.fr.md"}
VOICES = {
    "en": {"A": "en-US-AvaMultilingualNeural", "B": "en-US-AndrewMultilingualNeural"},
    "fr": {"A": "fr-CA-SylvieNeural", "B": "fr-CA-ThierryNeural"},
}
RATE = "+4%"
GAP_MS = 320
BITRATE = "48k"
MODEL = os.environ.get("PODCAST_MODEL", "claude-sonnet-5-5")
API_URL = os.environ.get("PODCAST_API_URL", "https://api.anthropic.com/v1/messages")


def bundles() -> list[Path]:
    """Post bundles plus top-level project pages (repository notes excluded)."""
    found = []
    for section in ("posts", "projects"):
        for d in sorted((CONTENT / section).iterdir()):
            if d.is_dir() and d.name != "notes" and (d / "index.md").exists():
                found.append(d)
    return found


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------- scripts

def page_text(md: str) -> str:
    """Front matter title/description plus body without shortcodes or code."""
    fm, body = "", md
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    if m:
        fm, body = m.group(1), md[m.end():]
    keep = [ln for ln in fm.splitlines() if ln.startswith(("title:", "description:", "tags:"))]
    body = re.sub(r"```.*?```", "[code block omitted]", body, flags=re.S)
    body = re.sub(r"\{\{[<%].*?[%>]\}\}", "", body, flags=re.S)
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body)
    body = re.sub(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", "", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", body)
    body = re.sub(r"<[^>]+>", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return ("\n".join(keep) + "\n\n" + body.strip())[:14000]


def call_claude(lang: str, source: str) -> dict:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set; cannot write new scripts")
    language = "English" if lang == "en" else "French (Canadian-friendly, natural register)"
    payload = {
        "model": MODEL,
        "max_tokens": 2500,
        "system": PROMPT.read_text(encoding="utf-8"),
        "messages": [{
            "role": "user",
            "content": f"Write the episode in {language}.\n\nSource page:\n\n{source}",
        }],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        body = json.loads(resp.read())
    text = "".join(b.get("text", "") for b in body["content"] if b.get("type") == "text")
    text = text[text.index("{"): text.rindex("}") + 1]
    data = json.loads(text)
    validate(data)
    return data


def validate(data: dict) -> None:
    lines = data.get("lines")
    if not isinstance(lines, list) or len(lines) < 4:
        raise ValueError("script needs at least 4 lines")
    for ln in lines:
        if ln.get("speaker") not in ("A", "B") or not str(ln.get("text", "")).strip():
            raise ValueError(f"bad line: {ln!r}")


def do_scripts(targets: list[Path], refresh_stale: bool) -> int:
    failures = 0
    for d in targets:
        for lang, src in LANGS.items():
            md_path = d / src
            if not md_path.exists():
                continue
            md = md_path.read_text(encoding="utf-8")
            h = sha(md)
            out = d / f"podcast.{lang}.json"
            data = load(out)
            if data and "source_hash" not in data:
                data["source_hash"] = h  # hand- or agent-written script: adopt it
                save(out, data)
                continue
            if data and (data["source_hash"] == h or not refresh_stale):
                continue
            rel = out.relative_to(ROOT)
            try:
                new = call_claude(lang, page_text(md))
            except Exception as exc:  # noqa: BLE001 - report and keep going
                print(f"  ! {rel}: {exc}", file=sys.stderr)
                failures += 1
                continue
            keep = {k: data[k] for k in ("duration_seconds", "audio_hash") if data and k in data}
            save(out, {"title": new.get("title", ""), "lines": new["lines"],
                       "source_hash": h, "model": MODEL, **keep})
            print(f"  script {rel}")
    return failures


# ----------------------------------------------------------------------- audio

def audio_hash(data: dict, lang: str) -> str:
    return sha(json.dumps([data["lines"], VOICES[lang], RATE, GAP_MS, BITRATE], ensure_ascii=False))


async def tts_lines(lines: list[dict], lang: str, tmp: Path) -> list[Path]:
    import edge_tts

    sem = asyncio.Semaphore(4)
    paths = [tmp / f"line{i:03d}.mp3" for i in range(len(lines))]

    async def one(i: int, ln: dict) -> None:
        async with sem:
            for attempt in range(4):
                try:
                    comm = edge_tts.Communicate(ln["text"], VOICES[lang][ln["speaker"]], rate=RATE)
                    await comm.save(str(paths[i]))
                    return
                except Exception:  # noqa: BLE001 - transient network errors
                    if attempt == 3:
                        raise
                    await asyncio.sleep(2 * (attempt + 1))

    await asyncio.gather(*(one(i, ln) for i, ln in enumerate(lines)))
    return paths


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def render(data: dict, lang: str, out: Path) -> None:
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        parts = asyncio.run(tts_lines(data["lines"], lang, tmp))
        gap = tmp / "gap.mp3"
        ffmpeg("-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono", "-t", str(GAP_MS / 1000),
               "-c:a", "libmp3lame", "-b:a", BITRATE, str(gap))
        listing = tmp / "list.txt"
        entries = []
        for p in parts:
            entries += [f"file '{p.as_posix()}'", f"file '{gap.as_posix()}'"]
        listing.write_text("\n".join(entries[:-1]) + "\n", encoding="utf-8")
        ffmpeg("-f", "concat", "-safe", "0", "-i", str(listing),
               "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ac", "1", "-ar", "24000",
               "-c:a", "libmp3lame", "-b:a", BITRATE, "-id3v2_version", "3",
               "-metadata", f"title={data.get('title', '')}",
               "-metadata", "artist=Antoine Boucher — audio story",
               str(out))


def do_audio(targets: list[Path], force: bool) -> int:
    if not shutil.which("ffmpeg"):
        print("ffmpeg not found on PATH", file=sys.stderr)
        return 1
    failures = 0
    for d in targets:
        for lang in LANGS:
            js = d / f"podcast.{lang}.json"
            data = load(js)
            if not data:
                continue
            mp3 = d / f"podcast.{lang}.mp3"
            ah = audio_hash(data, lang)
            if not force and mp3.exists() and data.get("audio_hash") == ah:
                continue
            rel = mp3.relative_to(ROOT)
            try:
                validate(data)
                render(data, lang, mp3)
            except Exception as exc:  # noqa: BLE001
                print(f"  ! {rel}: {exc}", file=sys.stderr)
                failures += 1
                continue
            data["audio_hash"] = ah
            data["duration_seconds"] = round(duration(mp3))
            save(js, data)
            print(f"  audio  {rel}  {data['duration_seconds']}s  {mp3.stat().st_size // 1024} KB")
    return failures


def do_check(targets: list[Path]) -> int:
    """Report pages without episodes and episodes whose source page changed."""
    issues = 0
    for d in targets:
        for lang, src in LANGS.items():
            if not (d / src).exists():
                continue
            rel = (d / src).relative_to(ROOT)
            data = load(d / f"podcast.{lang}.json")
            if not data:
                print(f"  missing script: {rel}")
                issues += 1
                continue
            if data.get("source_hash") and data["source_hash"] != sha((d / src).read_text(encoding="utf-8")):
                print(f"  stale script:   {rel}")
            if not (d / f"podcast.{lang}.mp3").exists() or data.get("audio_hash") != audio_hash(data, lang):
                print(f"  missing audio:  {rel}")
                issues += 1
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scripts", action="store_true", help="write missing scripts with Claude")
    ap.add_argument("--refresh-stale", action="store_true", help="also rewrite scripts whose page changed")
    ap.add_argument("--audio", action="store_true", help="render missing or outdated MP3s")
    ap.add_argument("--force-audio", action="store_true", help="re-render every MP3")
    ap.add_argument("--check", action="store_true", help="list missing or outdated episodes")
    ap.add_argument("--only", action="append", default=[], help="bundle folder name (repeatable)")
    args = ap.parse_args()

    targets = bundles()
    if args.only:
        targets = [d for d in targets if d.name in args.only]
    if not (args.scripts or args.audio or args.force_audio or args.check):
        ap.error("choose --scripts, --audio or --check")

    failures = 0
    if args.scripts:
        failures += do_scripts(targets, args.refresh_stale)
    if args.audio or args.force_audio:
        failures += do_audio(targets, args.force_audio)
    if args.check:
        n = do_check(targets)
        print(f"{n} episode(s) missing or outdated")
        failures += n
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
