import socket
import threading

# Server code
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[{client_address}] {message}")
            client_socket.send("Message received".encode('utf-8'))
    except ConnectionResetError:
        print(f"[DISCONNECT] {client_address} disconnected.")
    finally:
        client_socket.close()


def start_server():
    server_ip = "0.0.0.0"
    server_port = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen()
    print(f"[LISTENING] Server is listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Client code
def start_client():
    server_ip = "127.0.0.1"
    server_port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    def send_messages():
        while True:
            message = input("You: ")
            client.send(message.encode('utf-8'))

    thread = threading.Thread(target=send_messages)
    thread.start()

    try:
        while True:
            response = client.recv(1024).decode('utf-8')
            if not response:
                break
            print(f"Server: {response}")
    except ConnectionResetError:
        print("[DISCONNECTED] Server closed the connection.")
    finally:\
        client.close()

if __name__ == "__main__":
    mode = input("Enter 'server' to start server or 'client' to start client: ").strip().lower()
    if mode == 'server':
        start_server()
    elif mode == 'client':
        start_client()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")