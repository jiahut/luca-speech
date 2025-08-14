import http.server
import socketserver
import os
import json
import yaml

class AudioPlayerHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/audio-files':
            try:
                with open("config.yaml", "r") as f:
                    config = yaml.safe_load(f)
                output_dir = config.get("output_directory", "output")

                if not os.path.isdir(output_dir):
                    self.send_error(404, f"Output directory not found: {output_dir}")
                    return

                files = [f for f in os.listdir(output_dir) if f.endswith('.mp3')]

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(files).encode('utf-8'))

            except Exception as e:
                self.send_error(500, f"Server error: {e}")
        else:
            # Serve other files like index.html, style.css, script.js, and the audio files
            super().do_GET()

PORT = 8000
Handler = AudioPlayerHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    print(f"Open http://localhost:{PORT} in your browser.")
    httpd.serve_forever()
