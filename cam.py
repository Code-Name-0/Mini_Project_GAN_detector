import cv2
import asyncio
import websockets

# Camera settings
CAMERA_INDEX = 0  # Change this if your camera has a different index
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# API endpoint
API_ENDPOINT = "ws://localhost:8000/video_feed"

async def stream_video():
    # Open the laptop's camera
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    async with websockets.connect(API_ENDPOINT) as websocket:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break

            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Send the frame to the API
            await websocket.send(frame_bytes)

    # Release the camera
    cap.release()

# Start the video streaming
asyncio.get_event_loop().run_until_complete(stream_video())