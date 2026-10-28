#!/usr/bin/env python3
"""Local static server that serves 404.html for missing paths (like GitHub Pages)."""

from __future__ import annotations

import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class NotFoundHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str | None = None, not_found: Path | None = None, **kwargs):
        self._not_found = not_found
        super().__init__(*args, directory=directory, **kwargs)

    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        if code == 404 and self._not_found and self._not_found.is_file():
            try:
                body = self._not_found.read_bytes()
            except OSError:
                return super().send_error(code, message, explain)
            self.send_response(404, message or "File not found")
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        return super().send_error(code, message, explain)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", "-d", default="_site_loop", help="Site root to serve")
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--not-found",
        default="404.html",
        help="HTML file (relative to directory, or absolute) for HTTP 404 responses",
    )
    args = parser.parse_args()
    root = Path(args.directory).resolve()
    not_found = Path(args.not_found)
    if not not_found.is_absolute():
        not_found = root / not_found
    if not not_found.is_file():
        # Fall back to repo-root 404 if the served tree is missing one.
        candidate = Path(__file__).resolve().parents[2] / "404.html"
        if candidate.is_file():
            not_found = candidate

    handler = functools.partial(NotFoundHandler, directory=str(root), not_found=not_found)
    server = ThreadingHTTPServer((args.bind, args.port), handler)
    print(f"Serving {root} on http://{args.bind}:{args.port}/ (404 -> {not_found})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
