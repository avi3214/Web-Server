import socket 
import threading
import os
import webbrowser

HOST = socket.gethostbyname(socket.gethostname())
#clear
PORT = 4040
#PORT = 5050 

def server_setup():
    # creates a TPC socket and binds it to the local host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    return s

def handle_client(conn, addr):
    # parse HTTP GET request 
    data = conn.recv(1024)
    decoded_string = data.decode('utf-8')
    http_request = decoded_string.splitlines()
    
    request_line =  http_request[0]
    request_method, request_path, request_protocol = request_line.split()
    print(f"[REQUEST LINE] {request_line}")
    

    if request_method == "GET":
        requested_file = request_path.split('/')[-1]  # Assuming the path is in the format "/path/to/file.html"
        filename = 'localhost:'+str(PORT) + request_path
        webbrowser.open(filename)
        print(filename)
        # how to set up routes in a standard way 

def start():
    s = server_setup()
    # accepts new connections and creates a thread for each connection 
    while True: 
        conn, addr = s.accept() 
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def main():
    start()
    #print(HOST)

if __name__ == "__main__":
    main()
