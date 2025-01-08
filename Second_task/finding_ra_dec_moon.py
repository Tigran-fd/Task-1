import asyncio
import websockets
from pyngrok import ngrok

connected_clients = set()

async def handle_connection(websocket):
    connected_clients.add(websocket)
    print(f"New client connected: {websocket.remote_address}")

    try:
        while True:
            await websocket.send("Hello world!")
            await asyncio.sleep(10)
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        connected_clients.remove(websocket)

async def start_websocket_server():
    server = await websockets.serve(handle_connection, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")

    ngrok_tunnel = ngrok.connect(8765, "http")
    print(f"Ngrok tunnel URL: {ngrok_tunnel.public_url.replace('http', 'ws')}")
    print("Use the above URL to access the WebSocket server.")

    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_websocket_server())
