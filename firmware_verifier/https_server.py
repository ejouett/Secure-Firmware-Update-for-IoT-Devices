import http.server
import ssl

PORT = 8443

server_address = ('', PORT)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(
    httpd.socket,
    keyfile="key.pem",
    certfile="cert.pem",
    server_side=True
)

print(f"🔐 HTTPS server running at https://localhost:{PORT}")
httpd.serve_forever()
