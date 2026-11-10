# Audio stories (podcast episodes)

Every Hugo post and top-level project page can carry a short two-host audio
episode (about 1.5 to 3 minutes) in English and French.

| File in the page bundle | What it is |
|---|---|
| `podcast.en.json` / `podcast.fr.json` | Script (`title`, `lines` with speaker `A`/`B`) plus build metadata |
| `podcast.en.mp3` / `podcast.fr.mp3` | Rendered audio, mono 48 kbit/s |

`hugo/layouts/partials/podcast-player.html` shows the player and a collapsible
transcript under the article header when the MP3 for the page language exists.
Styles are at the end of `hugo/assets/editorial.css`.

## Generate

```bash
pip install edge-tts          # ffmpeg must be on PATH
python scripts/build/generate_podcasts.py --scripts --audio
python scripts/build/generate_podcasts.py --check
```

- `--scripts` writes missing scripts with Claude (`ANTHROPIC_API_KEY`,
  model from `PODCAST_MODEL`, default `claude-sonnet-5-5`). The style rules
  are in `scripts/build/podcast_prompt.md`. `--refresh-stale` also rewrites
  scripts whose source page changed since they were written.
- `--audio` renders MP3s with edge-tts voices (EN: Ava and Andrew; FR:
  Sylvie and Thierry, fr-CA) and only re-renders when a script or voice changes.
- `--only <bundle-folder>` limits a run to one page; repeatable.

Hand edits to a script are fine: run `--audio` afterwards to re-render it.
Repository notes under `projects/notes/` are included; their text is read from the built page in `docs/blog` because the body is a shortcode.
