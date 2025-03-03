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