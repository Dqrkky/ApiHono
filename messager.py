import asyncio
import threading
import websockets
import flask
import queue

# Flask app
app = flask.Flask(__name__)

# Queue for storing messages from WebSocket to be sent to SSE clients
message_queue = queue.Queue()
clients = []
clients_lock = threading.Lock()

# WebSocket client (runs in background)
async def websocket_client():
    uri = "wss://example.com/ws"  # Replace with your WebSocket URL
    async with websockets.connect(uri) as ws:
        print("Connected to WebSocket server")
        async for message in ws:
            message_queue.put(message)

# Background task to run WebSocket client
def start_websocket_loop():
    asyncio.new_event_loop().run_until_complete(websocket_client())

# SSE endpoint
@app.route('/events')
def sse():
    def event_stream():
        client_queue = queue.Queue()
        with clients_lock:
            clients.append(client_queue)
        try:
            yield ": connected\n\n"  # comment to force flush
            while True:
                data = client_queue.get()
                yield f'data: {data}\n\n'
        except GeneratorExit:
            with clients_lock:
                if client_queue in clients:
                    clients.remove(client_queue)
    return flask.Response(event_stream(), mimetype='text/event-stream')

# Distributor: broadcast WS messages to all connected SSE clients
def distribute_messages():
    while True:
        try:
            msg = message_queue.get(timeout=10)
        except queue.Empty:
            continue
        with clients_lock:
            for client in clients:
                client.put(msg)

# Launch everything
if __name__ == '__main__':
    threading.Thread(target=start_websocket_loop, daemon=True).start()
    threading.Thread(target=distribute_messages, daemon=True).start()
    app.run(host='0.0.0.0', port=9090, threaded=True)