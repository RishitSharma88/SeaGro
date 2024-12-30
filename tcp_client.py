import socket

TCP_SERVER_HOST = '127.0.0.1'  # Your TCP server
TCP_SERVER_PORT = 65432

def start_tcp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
        print("Connected to server.")
        
        while True:
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024)
            print(f"Response from server: {response.decode()}")

if __name__ == "__main__":
    start_tcp_client()
