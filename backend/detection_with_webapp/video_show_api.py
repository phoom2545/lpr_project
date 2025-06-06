from flask import Flask, Response
from flask_cors import CORS
import cv2
import time

app = Flask(__name__)
CORS(app)

video_path = 'MyVideo/video1.MOV'
# Create a frame with a format ready to be send frame by frame
def generate_frames():
    cap = cv2.VideoCapture(video_path)
    
    while True:
        success, frame = cap.read()

        # This will occur when frame is not read or video is ended.
        if not success:
            # Loop the video
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Reset to first frame. Therefore, this will playback the video infinitely
            continue
        
        # Encode frame from raw frame data as numpy array to jpeg format data but still a numpy array
        _, buffer = cv2.imencode('.jpg', frame)
        # Convert the numpy array to the byte format which is required by the HTTP protocol
        frame_bytes = buffer.tobytes()
        
        # Yield frame in multipart format (yield is like 'return' but it can pause and comeback not exit like return)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        
        time.sleep(0.033)  # ~30 FPS (it works on each frame 0.033 sec, which in 1 second it can process 30 frames meaning 30 FPS)

@app.route('/get_video_stream')
def get_video_stream():
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame') 
# The request calling this endpoint will be done only once but the response will continue forever (because the video is infinite)
# Response each frame at a time where next frame will replace the previous frame when the yield put '--frame' on top, the browser will acknowledge the new frame to process



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)