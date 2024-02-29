import socket 
import threading
import os
import webbrowser

HOST = socket.gethostbyname(socket.gethostname())
#clear
#PORT = 5050
PORT = 4040

def server_setup():
    # creates a TPC socket and binds it to the local host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    return s

def list_directory(directory):
    file_list = "<h1>Directory Listing</h1>"
    for filename in os.listdir(directory):
        file_list += f"<p>{filename}</p>"
    return file_list.encode('utf-8')

def handle_client(conn, addr):
    # parse HTTP GET request 
    data = conn.recv(1024)
    decoded_string = data.decode('utf-8')
  
    http_request = decoded_string.splitlines()
    
    request_line =  http_request[0]
    request_method, request_path, request_protocol = request_line.split()
    print(f"[REQUEST LINE]  {request_line}")
    print(f"[REQUEST PATH]  {request_path}")
    

    if request_method == "GET":
        current_directory = os.getcwd()
        print("DIRECTORY" + current_directory + request_path)
        requested_file = os.path.join(os.getcwd(), request_path[1:])
        print(requested_file)

        if os.path.isdir(requested_file):
            file_list = list_directory(requested_file)
            response = (
                f"HTTP/1.1 200 OK\n."
                +f"Content-Type: text/html\r\n"
                +f"Content-Length: {len(file_list)}\r\n"
                +f"\r\n"
            ).encode('utf-8') + file_list
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
        print("w1")
        conn, addr = s.accept() 
        print("w2")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        print("w3")
        thread.start()
        print('w4')
        # print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        continue

def main():
    start()
    #print(HOST)

if __name__ == "__main__":
    main()
