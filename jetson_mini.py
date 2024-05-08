import cv2
import asyncio
import websockets
from jetbotmini import Camera

# Camera settings
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# API endpoint
API_ENDPOINT = "ws://192.168.54.74:8000/video_feed"

async def stream_video():
    # Open the robot's camera
    camera = Camera.instance(width=FRAME_WIDTH, height=FRAME_HEIGHT)

    async with websockets.connect(API_ENDPOINT) as websocket:
        while True:
            # Capture frame from the camera
            frame = camera.value

            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Send the frame to the API
            await websocket.send(frame_bytes)

    # Stop the camera
    camera.stop()

# Start the video streaming
asyncio.get_event_loop().run_until_complete(stream_video())