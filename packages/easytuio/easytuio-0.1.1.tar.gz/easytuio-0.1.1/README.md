# EasyTUIO

EasyTUIO is a Python library for parsing and handling TUIO messages, used in multi-touch and tangible interfaces.

## Features
- Supports `2Dcur`, `2Dobj`, and `2Dblb` profiles.
- Customizable event listeners.
- Lightweight and easy to integrate.

## Installation
```bash
pip install easytuio
```

## Usage
```python
from easytuio import TUIOClient

def handle_cursor_event(cursor):
    print(f"Cursor Event: {cursor}")

client = TUIOClient()


client.register_callback("2Dcur", handle_cursor_event)
client.start()
```
