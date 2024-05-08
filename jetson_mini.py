import cv2
import asyncio
import websockets
from jetbotmini import Camera

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

API_ENDPOINT = "ws://192.168.54.74:8000/video_feed"

async def stream_video():
    camera = Camera.instance(width=FRAME_WIDTH, height=FRAME_HEIGHT)

    async with websockets.connect(API_ENDPOINT) as websocket:
        while True:
            frame = camera.value

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            await websocket.send(frame_bytes)

    camera.stop()

asyncio.get_event_loop().run_until_complete(stream_video())