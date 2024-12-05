def normalize_coordinates(x, y, width, height):
    """Normalize coordinates based on sensor dimensions."""
    return x / width, y / height
