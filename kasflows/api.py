from fastapi import FastAPI, Request
import uvicorn, threading, datetime
from kasflows.kasflows import Kasflows

app = FastAPI()
connections = {}

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
        connections[data["name"]] = {"token": data["token"], "time": datetime.datetime.now()}
        Kasflows.emit("connect", data)
        return {"status": "connected"}

@app.post("/getmessage")
async def getmessage(request: Request):
    data = await request.json()
    if data["name"] in Kasflows.messageforclient:
        message = Kasflows.messageforclient[data["name"]]
        Kasflows.emit("messageclient", {"name": data["name"], "message": message})
        return {"status": "success", "message": message}
    else:
        return {"status": "no message"}

@app.post("/sendmessage")
async def sendmessage(request: Request):
    data = await request.json()
    Kasflows.emit("messageserver", data)
    return {"status": "success"}

def start(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    uvicorn.run(app, host=host, port=port, reload=reload)