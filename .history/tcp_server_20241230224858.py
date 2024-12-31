import socket
import select

# Server configuration
HOST = '127.0.0.1'  # localhost
PORT = 12345        # Port to listen on

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Chat server started on {HOST}:{PORT}")

# List of sockets for select
sockets_list = [server_socket]

# Dictionary to store clients and their usernames
clients = {}

def broadcast(message, sender_socket):
    """Send a message to all connected clients except the sender."""
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                client_socket.close()
                sockets_list.remove(client_socket)
                del clients[client_socket]

def handle_new_connection():
    """Accept a new client connection."""
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")
    client_socket.send(b"Enter your username: ")
    sockets_list.append(client_socket)
    clients[client_socket] = None  # Username will be set after the client sends it

def handle_client_message(client_socket):
    """Handle a message from a client."""
    try:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            raise ConnectionResetError()

        # If username is not set, set it
        if clients[client_socket] is None:
            clients[client_socket] = message.strip()
            print(f"User '{clients[client_socket]}' joined the chat.")
            client_socket.send(b"Welcome to the chat!\n")
            broadcast(f"{clients[client_socket]} has joined the chat.\n".encode('utf-8'), client_socket)
        else:
            # Broadcast the message to other clients
            broadcast(f"{clients[client_socket]}: {message}\n".encode('utf-8'), client_socket)

    except (ConnectionResetError, ConnectionAbortedError):
        print(f"Connection with {clients[client_socket]} closed.")
        broadcast(f"{clients[client_socket]} has left the chat.\n".encode('utf-8'), client_socket)
        sockets_list.remove(client_socket)
        del clients[client_socket]
        client_socket.close()

try:
    while True:
        # Use select to monitor sockets for readiness
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                handle_new_connection()
            else:
                handle_client_message(notified_socket)

except KeyboardInterrupt:
    print("\nServer shutting down.")

finally:
    server_socket.close()
