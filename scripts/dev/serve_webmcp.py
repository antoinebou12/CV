"""Serve the built site at /CV/ on loopback for local WebMCP development."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

class PreviewServer(ThreadingHTTPServer):
    request_queue_size = 128

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def translate_path(self, path):
        route = urlsplit(path).path
        if route == '/CV' or route.startswith('/CV/'):
            return super().translate_path(route[3:] or '/')
        return str(Path(self.directory) / '__webmcp_not_found__')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8934)
    args = parser.parse_args()
    site = Path(__file__).resolve().parents[2] / 'docs'
    if not (site / 'index-en.html').is_file():
        parser.error('Build docs with scripts/deploy/publish_site.py first.')
    PreviewServer(('127.0.0.1', args.port), partial(Handler, directory=str(site))).serve_forever()
