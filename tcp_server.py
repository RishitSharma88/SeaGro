import socket
import threading

TCP_SERVER_HOST = '127.0.0.1'  # Your TCP server
TCP_SERVER_PORT = 65432

clients = []  # List to store all connected clients

def handle_client(client_socket, client_address):
    print(f"Client {client_address} connected.")
    try:
        while True:
            # Receive message from client
            message = client_socket.recv(1024)
            if not message:
                break  # Client disconnected
            print(f"Message from {client_address}: {message.decode()}")
            
            # Forward the message to all other connected clients
            for client in clients:
                if client != client_socket:  # Don't send the message back to the sender
                    try:
                        client.sendall(message)
                    except:
                        continue

    finally:
        # Remove the client from the list and close the connection
        clients.remove(client_socket)
        client_socket.close()
        print(f"Client {client_address} disconnected.")

def start_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((TCP_SERVER_HOST, TCP_SERVER_PORT))
        server_socket.listen()
        print(f"TCP server started on {TCP_SERVER_HOST}:{TCP_SERVER_PORT}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)  # Add client to the list
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    start_tcp_server()
