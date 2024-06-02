import http.server
import socketserver

# Define the handler to manage incoming requests
Handler = http.server.SimpleHTTPRequestHandler

# Define the port number
PORT = 8000
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    # Run the server, handling requests until you stop it with a keyboard interrupt (Ctrl+C)
    httpd.serve_forever()