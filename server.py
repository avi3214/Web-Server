import socket 
import threading

# 
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050

def server_setup():
    # creates a TPC socket and binds it to the local host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    return s

def handle_client(conn, addr):
    data = conn.recv(1024)
    if not data: 
        break
    conn.sendall(data)
    

def start():
    s = server_setup()
    # accepts new connections and creates a thread for each connection 
    while True: 
        conn, addr = s.accept() 
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def main():
    start()
    #print(HOST)

if __name__ == "__main__":
    main()
