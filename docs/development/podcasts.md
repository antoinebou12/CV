# Audio stories (podcast episodes)

Every Hugo post, project page and project note carries a short two-host audio
episode in English and French. Two hosts explain what the page is about, why
the work exists and how it works, in one to three minutes.

## What lives where

| Path | Role |
|---|---|
| `<page bundle>/podcast.en.json`, `podcast.fr.json` | Script: `title` and `lines` (speaker `A` or `B`), plus build metadata |
| `<page bundle>/podcast.en.mp3`, `podcast.fr.mp3` | Rendered audio, mono, 48 kbit/s |
| `scripts/build/generate_podcasts.py` | Writes missing scripts and renders audio |
| `scripts/build/podcast_prompt.md` | Style guide given to the model that writes scripts |
| `hugo/layouts/partials/podcast-player.html` | Player, speed button, download link and transcript |
| `hugo/assets/podcast-player.js` | Playback-speed button (remembers the choice) |
| `hugo/assets/editorial.css` | Player styles (search for `podcast-player`) |

The player appears under the article header on posts and project pages, and
under the title block on project notes. It only renders when the MP3 for the
page language exists. Post cards on list pages show an "Audio story" badge with
the duration.

## Everyday tasks

Requirements: Python 3, `pip install edge-tts`, and `ffmpeg` on the PATH.

```bash
python scripts/build/generate_podcasts.py --check
```

Lists pages without an episode, scripts whose page changed, and audio that no
longer matches its script.

```bash
python scripts/build/generate_podcasts.py --audio
```

Renders every missing or outdated MP3. It is incremental: an episode is only
rendered again when its lines or the voices change. A network drop during
text-to-speech fails only that episode; run the command again to retry.

```bash
python scripts/build/generate_podcasts.py --scripts --audio --only my-post-folder
```

Writes the script for one new page and renders it. `--only` takes the bundle
folder name and can be repeated.

### Writing scripts

- `--scripts` writes scripts that do not exist yet. It calls the Claude API and
  needs `ANTHROPIC_API_KEY`. `PODCAST_MODEL` overrides the model.
- `--refresh-stale` also rewrites scripts whose source page changed.
- Project notes render their body from a shortcode, so their text is read from
  the built page in `docs/blog`. Build the site first for a new note.
- A script written by hand, or by another tool, is adopted as it is: keep only
  `title` and `lines`, then run `--audio`.

### Editing an episode

Open the JSON, change the lines, then run `--audio`. Lines alternate between
speaker `A` (leads the story) and `B` (asks what a listener would ask).

## Style rules, in short

The full rules are in `scripts/build/podcast_prompt.md`.

- Explain what the work does and how it works. Do not dwell on bugs, limits or
  what is missing.
- Open with a hook, tell the story in plain words, give one concrete detail
  from the page, and close on what the listener learns.
- Use only facts from the page. Thin pages get shorter episodes.
- French episodes are written from the French page, not translated line by line.
- Antoine is referred to as "he" / "il" and is never one of the hosts.

## Voices

| Language | Host A | Host B |
|---|---|---|
| English | `en-US-AvaMultilingualNeural` (Ava) | `en-US-AndrewMultilingualNeural` (Andrew) |
| French | `fr-CA-SylvieNeural` (Sylvie) | `fr-CA-ThierryNeural` (Thierry) |

Change them in `VOICES` at the top of `generate_podcasts.py`. Every episode is
rendered again after a voice change. Update the host names in
`podcast-player.html` to match.

## Publishing

`scripts/deploy/build_docs.py` copies the scripts and MP3s into `docs/blog`
with the rest of the site, so the audio is stored twice in git (page bundle
and `docs/`). See also [blog-embeds.md](blog-embeds.md) for live demos and 3D
models.
