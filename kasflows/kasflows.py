import logging

class Kasflows:
    def __init__(self):
        self.eventsCallbacks = {
            "connect": [],
            "disconnect": [],
            "messageserver": [],
            "messageclient": []
        }
        self.messageforclient = {}

        self.on("connect", lambda data: print(f"Connected: {data}"))
        self.on("disconnect", lambda data: print(f"Disconnected: {data}"))
        self.on("messageserver", lambda data: print(f"Message from server: {data}"))
        self.on("messageclient", lambda data: print(f"Message to client: {data}"))

    def on(self, event: str, callback: callable):
        if event in self.eventsCallbacks:
            self.eventsCallbacks[event].append(callback)
            logging.info(f"Callback added for event '{event}'")
        else:
            raise ValueError(f"Event '{event}' is not supported")

    def off(self, event: str, callback: callable):
        if event in self.eventsCallbacks:
            self.eventsCallbacks[event].remove(callback)
            logging.info(f"Callback removed for event '{event}'")
        else:
            raise ValueError(f"Event '{event}' is not supported")

    def emit(self, event: str, data: dict, *args, **kwargs):
        if event in self.eventsCallbacks:
            for callback in self.eventsCallbacks[event]:
                callback(data, *args, **kwargs)
            logging.info(f"Event '{event}' emitted with data: {data}")
        else:
            raise ValueError(f"Event '{event}' is not supported")

Kasflows = Kasflows()