import os

from .vision import VisionClient

host = os.getenv("VISION_SERVICE_HOST", "localhost")
port = int(os.getenv("VISION_SERVICE_PORT", "9500"))

vision_client = VisionClient(host, port)
