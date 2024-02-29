import webbrowser
import http.server
import socketserver
import os

# Set the directory where your HTML files are located
root_directory = '/'

# Define the port number
port = 8000

# Change the current working directory to serve files from there
os.chdir(root_directory)

# Create a simple HTTP server
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", port), Handler) as httpd:
    print("Serving at port", port)
    
    # Open the web browser to the local server
    webbrowser.open_new_tab(f'http://localhost:{port}')

    # Serve the directory
    httpd.serve_forever()