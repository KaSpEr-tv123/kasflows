import logging

class Kasflows:
    def __init__(self):
        self.eventsCallbacks = {}
        self.messageforclient = {}

    def on(self, event: str, callback: callable):
            self.eventsCallbacks[event] = callback
            logging.info(f"Callback added for event '{event}'")

    def off(self, event: str):
            del self.eventsCallbacks[event]
            logging.info(f"Callback removed for event '{event}'")

    def emit(self, event: str, data: dict):
        if event in self.eventsCallbacks:
            self.eventsCallbacks[event](data)
            logging.info(f"Event '{event}' emitted with data: {data}")
        else:
            raise ValueError(f"Event '{event}' is not supported")

Kasflows = Kasflows()