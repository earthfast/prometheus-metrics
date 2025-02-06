from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.parse
import re

class MonitorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse threshold from query parameter (in GB)
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            threshold_gb = float(params.get('threshold', [10])[0])
            threshold_bytes = threshold_gb * 1000000000  # Convert GB to bytes

            # Get metrics from node-exporter
            metrics = urllib.request.urlopen('http://node-exporter:9100/metrics').read().decode()
            
            # Find root filesystem free bytes
            match = re.search(r'node_filesystem_free_bytes{device="/dev/root".*?} ([0-9.e+]+)', metrics)
            if not match:
                self.send_error(500, "Could not find disk space metric")
                return
            
            free_bytes = float(match.group(1))
            message = f"Disk space OK: {free_bytes/1000000000:.2f}GB free, threshold: {threshold_gb}GB"
            
            if free_bytes < threshold_bytes:
                self.send_response(500)
                message = f"Low disk space: {free_bytes/1000000000:.2f}GB free, threshold: {threshold_gb}GB"
            else:
                self.send_response(200)

            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(message.encode())))
            self.end_headers()
            self.wfile.write(message.encode())

        except Exception as e:
            self.send_error(500, str(e))

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9500), MonitorHandler)
    print("Starting disk monitor on port 9500...")
    server.serve_forever()


