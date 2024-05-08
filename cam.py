import cv2
import asyncio
import websockets

CAMERA_INDEX = 0  
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

API_ENDPOINT = "ws://localhost:8000/video_feed"

async def stream_video():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    async with websockets.connect(API_ENDPOINT) as websocket:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            await websocket.send(frame_bytes)

    cap.release()

asyncio.get_event_loop().run_until_complete(stream_video())