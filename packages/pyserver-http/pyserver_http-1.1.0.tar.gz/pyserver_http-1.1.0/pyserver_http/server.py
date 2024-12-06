import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

class FileServerHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        """Serve files from the ~/.pyserver directory."""
        base_dir = os.path.expanduser("~/.pyserver")
        rel_path = path.lstrip("/")
        return os.path.join(base_dir, rel_path)

def start_server(host="0.0.0.0", port=8000):
    os.makedirs(os.path.expanduser("~/.pyserver"), exist_ok=True)
    server_address = (host, port)
    httpd = HTTPServer(server_address, FileServerHandler)
    print(f"Serving on {host}:{port}")
    httpd.serve_forever()
