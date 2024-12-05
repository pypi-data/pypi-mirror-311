from easytuio import TUIOClient


def handle_cursor_event(cursor):
    print(f"Cursor Event: {cursor}")


def handle_object_event(obj):
    print(f"Object Event: {obj}")


if __name__ == "__main__":
    client = TUIOClient()
    client.register_callback("2Dcur", handle_cursor_event)
    client.register_callback("2Dobj", handle_object_event)

    client.start()
