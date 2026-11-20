"""
No-cache HTTP server for development.
Serves files with Cache-Control: no-store to prevent browser caching.
"""
import http.server
import sys

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = http.server.HTTPServer(('', port), NoCacheHTTPRequestHandler)
    print(f'Serving on http://localhost:{port} (no-cache)')
    server.serve_forever()
