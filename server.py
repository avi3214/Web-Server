# David Nguyen
# 1001837746 

import socket     # socket library used for networking 
import threading  # thread library used for multiple executions of code
import os         # os library used for file system opreations

HOST = "127.0.0.1" # loopback interface address 
PORT = 4040        

# this function creates a TPC socket and binds it to the local host and port 
# returns a socket object 
def server_setup():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a socket to listen to 
    s.bind((HOST, PORT)) # binds socket to host and port
    s.listen(5) # socket can listen to at most 5 connections 
    #print(f"Server listening on {HOST}:{PORT}")
    return s

# takes in http request path as input 
# returns an HTML page of the local directory 
def show_directory(path):
    files = "<h1>Directory</h1>"  # convert directory listing as HTML object 
    for file in path:   
        files += f"<p>{file}</p>" # for every file in the directory, create a HTML listing
    return files.encode('utf-8')  # encode HTML as bytes 

# function handles http request made by the client 
def handle_client(conn, addr):
    data = conn.recv(1024)  # Receives http request from the web browser 
    decoded_string = data.decode('utf-8') # data is recieved in bytes
                                          # converts bytes into strings       

    http_request = decoded_string.splitlines() # parses the http request 
    request_line =  http_request[0] # Request line represents the first line of the request
    request_method, request_path, request_protocol = request_line.split() # obtain the method, path, and protocol sent from 
    #print(f"[REQUEST LINE]  {request_line}")
    #print(f"[REQUEST PATH]  {request_path}")
    
    
    response = f"" # prepare the response to http request 
    if request_method == "GET":
        # retrieve the local file directory 
        current_directory = os.getcwd() # get the local file directory 
        #print("DIRECTORY" + current_directory + request_path)
        requested_file = os.path.join(os.getcwd(), request_path[1:]) # create an absolute path for requested file
        #print(requested_file)

        if os.path.isdir(requested_file):  # check if http request path is a directory 
            directory_list = os.listdir(requested_file) # list all files in the directory 
            file_list = show_directory(directory_list)  # create an HTML response page of the directory 
            response = (
                f"HTTP/1.1 200 OK\n"
                +f"Content-Type: text/html\n"
                +f"Content-Length: {len(file_list)}\r\n"
                +f"\r\n"
            ).encode('utf-8') + file_list # respond to http request in bytes   
        elif os.path.isfile(requested_file): # check to see if the http requests an actual file
            with open(requested_file, 'rb') as file: # obtain the contents of said file in bytes 
                file_data = file.read()
                # the 200 response is sent back along with the requested file 
                response = (
                    f"HTTP/1.1 200 OK\n"
                    +f"Content-Type: text/html\n"
                    +f"Content-Length: {len(file_data)}\r\n"
                    +f"\r\n"
                ).encode('utf-8') + file_data 
        # check the requested file in a specific page1.html and redirect to page2.html 
        elif requested_file == "http://localhost:6789/page1.html":
            with open("page2.html", 'rb') as redirect_file:
                file_data = redirect_file.read()
                response = (
                        f"HTTP/1.1 200 OK\n"
                        +f"Content-Type: text/html\n"
                        +f"Content-Length: {len(file_data)}\r\n"
                        +f"\r\n"
                    ).encode('utf-8') + file_data
        else:
            with open("404.html", 'rb') as not_found_file:
                file_data = not_found_file.read()
                # send back http request with status code 404 
                response = (
                        f"HTTP/1.1 404 Not Found\n"
                        +f"Content-Type: text/html\n"
                        +f"Content-Length: {len(file_data)}\r\n"
                        +f"\r\n"
                    ).encode('utf-8') + file_data
        
        conn.sendall(response) # send specified http request back to http request 
    conn.close() # once the response is sent, close the connection to client 

# accepts new connections and creates a thread for each connection 
def start():
    s = server_setup() # set up the socket object as a server 
    while True: 
        #print("w1")
        conn, addr = s.accept() # blocks execution of program until a new connection request is made 
        #print("w2")
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # creates a thread to handle new connection
        #print("w3")
        thread.start()
        #print('w4')
    
def main():
    start()

if __name__ == "__main__":
    main()
