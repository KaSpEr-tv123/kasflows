### **KasFlows Documentation**  

KasFlows is a lightweight event-driven communication system designed as an alternative to WebSockets, specifically created for Roblox cheats scripts. It provides a simple and flexible way to handle client-server communication using FastAPI.  

---

## **Installation**  

```bash
pip install kasflows
```

---

## **Core Components**  

The library consists of two main components:  

1. **KasFlows API Server (`api.py`)**  
   - Manages client connections and disconnections.  
   - Handles message exchange between clients and server.  
   - Automatically disconnects inactive clients after **10 seconds**.  
   - Provides a simple HTTP API for sending and receiving messages.  

2. **KasFlows Event System (`kasflows.py`)**  
   - Provides an event-driven architecture.  
   - Supports event registration (`on`), removal (`off`), and triggering (`emit`).  
   - Handles four main events:
     - `connect` – Triggered when a client connects.  
     - `disconnect` – Triggered when a client disconnects.  
     - `messageserver` – Triggered when the server receives a message.  
     - `messageclient` – Triggered when a client receives a message.  

---

## **Basic Usage**  

### **1. Starting the Server**  
The API server is built with FastAPI and can be started using the `start()` function.  

```python
from kasflows import start

# Start the server on localhost:8000
start(host="127.0.0.1", port=8000)
```

---

### **2. Event Handling**  

KasFlows uses an event-driven system to handle client interactions.  

#### **Registering Event Handlers**  

```python
from kasflows import Kasflows

def on_connect(data):
    print(f"Client connected: {data}")

def on_message(data):
    print(f"Message from {data['name']}: {data['message']}")

# Register event handlers
Kasflows.on("connect", on_connect)
Kasflows.on("messageserver", on_message)
```

#### **Removing Event Handlers**  

```python
Kasflows.off("connect", on_connect)
Kasflows.off("messageserver", on_message)
```

#### **Manually Emitting Events**  

```python
Kasflows.emit("messageserver", {"name": "client1", "message": "Hello"})
```

---

## **API Endpoints**  

KasFlows provides simple HTTP endpoints for handling client communication.  

### **1. Client Connection (`POST /statusws`)**  

**Request:**  

```json
{
  "name": "client_name",
  "token": "client_token"
}
```

**Response:**  

```json
{
  "status": "connected"
}
```
or  
```json
{
  "status": "already connected"
}
```

---

### **2. Sending Messages (`POST /sendmessage`)**  

**Request:**  

```json
{
  "name": "client_name",
  "message": "Hello from client!"
}
```

**Response:**  

```json
{
  "status": "success"
}
```

---

### **3. Receiving Messages (`POST /getmessage`)**  

**Request:**  

```json
{
  "name": "client_name"
}
```

**Response (when message available):**  

```json
{
  "status": "success",
  "message": "Hello from server!"
}
```

**Response (when no message available):**  

```json
{
  "status": "no message"
}
```

---

## **Features**  

✅ **Automatic Client Disconnection** – Clients are removed if inactive for **10 seconds**.  
✅ **Event-Driven Architecture** – Uses `on`, `off`, and `emit` for handling events.  
✅ **Simple HTTP Interface** – Easy-to-use endpoints for client communication.  
✅ **Built-in Logging** – Logs events, connections, and messages.  

---

## **Example: Full Implementation**  

```python
from kasflows import Kasflows, start

# Define event handlers
def on_connect(data):
    print(f"New connection: {data}")

def on_disconnect(data):
    print(f"Client disconnected: {data}")

def on_message(data):
    print(f"Received message from {data['name']}: {data['message']}")

# Register events
Kasflows.on("connect", on_connect)
Kasflows.on("disconnect", on_disconnect)
Kasflows.on("messageserver", on_message)

# Start server
start(host="127.0.0.1", port=8000)
```

---

## **License**  

KasFlows is released under the **MIT License**.  