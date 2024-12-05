from pythonosc.osc_bundle import OscBundle
from pythonosc.osc_message import OscMessage
from .profiles import TUIO2DCursor, TUIO2DObject, TUIO2DBlob


class TUIOParser:
    def __init__(self):
        # Default event listeners
        self.listeners = {
            "SOURCE": self._handle_source,
            "UNKNOWN": self._handle_unknown,
        }

    def register_listener(self, event_type, callback):
        """Register a callback for a specific event type."""
        self.listeners[event_type] = callback

    def parse_tuio_message(self, data):
        """Parse OSC messages and extract TUIO events."""
        messages = []
        try:
            bundle = OscBundle(data)
            for content in bundle:
                if isinstance(content, OscMessage):
                    address = content.address
                    args = content.params

                    # Handle known TUIO message types
                    if address.startswith("/tuio/2Dcur"):
                        self._handle_2dcur(args, messages)
                    elif address.startswith("/tuio/2Dobj"):
                        self._handle_2dobj(args, messages)
                    elif address.startswith("/tuio/2Dblb"):
                        self._handle_2dblb(args, messages)

                    # Handle source messages
                    elif address.startswith("/tuio/source"):
                        self.listeners.get("SOURCE", self._handle_source)(args)

                    # Handle unknown messages
                    else:
                        self.listeners.get("UNKNOWN", self._handle_unknown)(address, args)
        except Exception as e:
            # Log or handle parsing errors here
            pass
        return messages

    def _handle_2dcur(self, args, messages):
        if args[0] == "set":
            messages.append(("2Dcur", TUIO2DCursor.from_osc(args[1:])))

    def _handle_2dobj(self, args, messages):
        if args[0] == "set":
            messages.append(("2Dobj", TUIO2DObject.from_osc(args[1:])))

    def _handle_2dblb(self, args, messages):
        if args[0] == "set":
            messages.append(("2Dblb", TUIO2DBlob.from_osc(args[1:])))

    def _handle_source(self, args):
        """Handle source messages (override if needed)."""
        pass

    def _handle_unknown(self, address, args):
        """Handle unknown messages (override if needed)."""
        pass
