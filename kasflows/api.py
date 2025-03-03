from fastapi import FastAPI, Request
import uvicorn, threading, datetime
from kasflows.kasflows import Kasflows
import requests

app = FastAPI()
connections = {}

class Client(Kasflows):
    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def emit(self, event, data):
        requests.post(self.url, json={"event": event, "data": data})

def disconnect_checker():
    while True:
        current_time = datetime.datetime.now()
        to_disconnect = []
        for name, info in connections.items():
            last_time = info["time"]
            if (current_time - last_time).total_seconds() > 10:
                to_disconnect.append(name)
        
        for name in to_disconnect:
            del connections[name]
            Kasflows.emit("disconnect", {"name": name})
        
        threading.Event().wait(5)

threading.Thread(target=disconnect_checker, daemon=True).start()

@app.post("/statusws")
async def checkws(request: Request):
    data = await request.json()
    if data["name"] in connections:
        connections[data["name"]]["time"] = datetime.datetime.now()
        return {"status": "already connected"}
    else:
        connections[data["name"]] = {"time": datetime.datetime.now()}
        Kasflows.emit("connect", data)
        return {"status": "connected"}

@app.post("/disconnect")
async def disconnect(request: Request):
    data = await request.json()
    if data["name"] in connections:
        del connections[data["name"]]
        Kasflows.emit("disconnect", data)
        return {"status": "disconnected"}
    else:
        return {"status": "not connected"}

@app.post("/getmessage")
async def getmessage(request: Request):
    data = await request.json()
    if data["name"] in Kasflows.messageforclient:
        message = Kasflows.messageforclient[data["name"]]
        return {"status": "success", "message": message}
    else:
        return {"status": "no message"}

@app.post("/sendmessage")
async def sendmessage(request: Request):
    data = await request.json()
    Kasflows.emit(data["event"], data["data"])
    return {"status": "success"}

@app.post("/sendmessagetoclient")
async def sendmessagetoclient(request: Request):
    data = await request.json()
    Kasflows.messageforclient[data["name"]] = data["message"]
    return {"status": "success"}

@app.get("/getclients")
async def getclients():
    return {"clients": connections}

def start(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    uvicorn.run(app, host=host, port=port, reload=reload)