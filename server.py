import socket 
import threading
import os
import webbrowser

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050

def server_setup():
    # creates a TPC socket and binds it to the local host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    return s

def show_directory(path):
    files = "<h1>Directory</h1>"
    for file in path:
        files += f"<p>{file}</p>"
    return files.encode('utf-8')

def handle_client(conn, addr):
    # parse HTTP GET request 
    data = conn.recv(1024)
    decoded_string = data.decode('utf-8')
  
    http_request = decoded_string.splitlines()
    
    request_line =  http_request[0]
    request_method, request_path, request_protocol = request_line.split()
    print(f"[REQUEST LINE]  {request_line}")
    print(f"[REQUEST PATH]  {request_path}")
    
    response = b""
    if request_method == "GET":
        # retrieve the local file directory 
        current_directory = os.getcwd()
        print("DIRECTORY" + current_directory + request_path)
        requested_file = os.path.join(os.getcwd(), request_path[1:])
        print(requested_file)

        if os.path.isdir(requested_file):
            directory_list = os.listdir(requested_file)
            file_list = show_directory(directory_list)
            response = (
                f"HTTP/1.1 200 OK\n"
                +f"Content-Type: text/html\n"
                +f"Content-Length: {len(file_list)}\r\n"
                +f"\r\n"
            ).encode('utf-8') + file_list

        elif os.path.isfile(requested_file):
            with open(requested_file, 'rb') as file:
                file_data = file.read()
                response = (
                    f"HTTP/1.1 200 OK\n"
                    +f"Content-Type: text/html\n"
                    +f"Content-Length: {len(file_data)}\r\n"
                    +f"\r\n"
                ).encode('utf-8') + file_data

        conn.sendall(response)

        #conn.sendall(b"HTTP/1.1 200 OK\n"
         #+b"Content-Type: text/html\n"
         #+b"\n" # Important!
         #+b"<html><body>Hello World</body></html>\n")
    
    conn.close()

def start():
    s = server_setup()
    # accepts new connections and creates a thread for each connection 
    while True: 
        #print("w1")
        conn, addr = s.accept() 
        #print("w2")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        #print("w3")
        thread.start()
        #print('w4')
    
def main():
    start()

if __name__ == "__main__":
    main()

"""
SOURCES
https://stackoverflow.com/questions/9752521/sending-utf-8-with-sockets
https://www.w3schools.com/python/module_os.asp
https://stackoverflow.com/questions/10114224/how-to-properly-send-http-response-with-python-using-socket-library-only
https://www.geeksforgeeks.org/python-list-files-in-a-directory/
https://www.youtube.com/watch?v=3QiPPX-KeSc&t=2211s
https://hackernoon.com/resolving-typeerror-a-bytes-like-object-is-required-not-str-in-python
https://www.quora.com/How-do-I-put-HTML-inside-a-Python-string
"""