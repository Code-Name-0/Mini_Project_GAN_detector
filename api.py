from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
import numpy as np

app = FastAPI()

@app.websocket("/video_feed")
async def video_feed(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            frame_bytes = await websocket.receive_bytes()
            frame = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # Display the frame (you can modify this part to suit your needs)
            cv2.imshow("Live Stream", frame)
            if cv2.waitKey(1) == ord('q'):
                break
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    finally:
        cv2.destroyAllWindows()

# Start the API server
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)