from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
import numpy as np
import os
import uvicorn

# Import model here

app = FastAPI()

@app.websocket("/video_feed")
async def video_feed(websocket: WebSocket):
    await websocket.accept()
    try:
        frame_counter = 0
        while True:
            frame_bytes = await websocket.receive_bytes()
            frame = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            output_path = os.path.join("./output/vis", f"frame_{frame_counter}.jpg")
            processed_frame = call_to_model(frame, output_path)

            cv2.imshow("Processed Stream", processed_frame)
            if cv2.waitKey(1) == ord('q'):
                break

            frame_counter += 1

    except WebSocketDisconnect:
        print("WebSocket connection closed")
    finally:
        cv2.destroyAllWindows()


uvicorn.run(app, host="0.0.0.0", port=8000)