import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from database_handler import initialize_db, update_dashboard_data, get_dashboard_data

class DashboardGatewayHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/ingest':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))
            
            subgroup = payload.get("source")
            data = payload.get("data")
            
            update_dashboard_data(subgroup, data)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Data aggregated successfully")

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(get_dashboard_data()).encode('utf-8'))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    initialize_db()
    server_address = ('', 8000)
    httpd = ThreadedHTTPServer(server_address, DashboardGatewayHandler)
    print("Server running on port 8000")
    httpd.serve_forever()