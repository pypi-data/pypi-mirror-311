import socket
from .messages import TUIOParser


class TUIOClient:
    def __init__(self, host="0.0.0.0", port=3333):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.parser = TUIOParser()
        self.callbacks = {}

    def register_callback(self, profile, callback):
        """Register a callback for a specific TUIO profile."""
        if profile not in self.callbacks:
            self.callbacks[profile] = []
        self.callbacks[profile].append(callback)

    def start(self):
        """Start listening for TUIO messages."""
        self.socket.bind((self.host, self.port))
        print(f"Listening for TUIO messages on {self.host}:{self.port}")
        while True:
            data, _ = self.socket.recvfrom(1024)
            self.handle_message(data)

    def handle_message(self, data):
        """Handle incoming TUIO messages."""
        messages = self.parser.parse_tuio_message(data)
        for profile, message in messages:
            if profile in self.callbacks:
                for callback in self.callbacks[profile]:
                    callback(message)
