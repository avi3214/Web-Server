import socket 
import threading
import os


HOST = socket.gethostbyname(socket.gethostname())
PORT = 4040

def server_setup():
    # creates a TPC socket and binds it to the local host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    return s

# returns an HTML page of the local directory 
def show_directory(path):
    files = "<h1>Directory</h1>"
    for file in path:
        files += f"<p>{file}</p>"
    return files.encode('utf-8')

def handle_client(conn, addr):
    # Receives http request from the web browser 
    data = conn.recv(1024)
    # data is recieved in bytes
    # converts bytes into strings 
    decoded_string = data.decode('utf-8')
  
    # parses the http request 
    http_request = decoded_string.splitlines()
    request_line =  http_request[0]
    request_method, request_path, request_protocol = request_line.split()
    #print(f"[REQUEST LINE]  {request_line}")
    #print(f"[REQUEST PATH]  {request_path}")
    
    response = f""
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
        else:
            response = (
                    f"HTTP/1.1 404 Not Found\n"
                    +f"Content-Type: text/html\n"
                    +f"\r\n"
                ).encode('utf-8')

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
