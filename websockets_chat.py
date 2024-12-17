import asyncio
import websockets
import socket

TCP_SERVER_HOST = '127.0.0.1'  # Your TCP server
TCP_SERVER_PORT = 65432
WEBSOCKET_PORT = 6789          # WebSocket port

async def websocket_handler(websocket, path):
    print("WebSocket connected")
    try:
        # Connect to TCP server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
            while True:
                # Receive message from browser via WebSocket
                message = await websocket.recv()
                print(f"Received from browser: {message}")

                # Forward message to TCP server
                tcp_socket.sendall(message.encode())

                # Get response from TCP server
                response = tcp_socket.recv(1024).decode()
                print(f"Response from TCP server: {response}")

                # Send response back to browser
                await websocket.send(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("WebSocket disconnected")

# Start WebSocket server
async def main():
    print(f"WebSocket server started on ws://localhost:{WEBSOCKET_PORT}")
    async with websockets.serve(websocket_handler, "localhost", WEBSOCKET_PORT):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
