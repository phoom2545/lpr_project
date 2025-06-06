from flask import Flask, Response,jsonify, request, send_file
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
import time
import io


app = Flask(__name__)
CORS(app)


frame_path = 'MyPhoto/test2.jpg'
# source_path = 'MyVideo/video1.MOV'




@app.route('/get_image')
def get_image():
    frame = cv2.imread(frame_path) # Raw pixel data which is numpy array with shape:(height, width, channels) in BGR color format

    # Image encoding (compress raw pixel data into JPEG format)
        # Input:    Raw numpy array
        # Output:   Tuple of (success_flag, encoded_bytes)
    _, buffer = cv2.imencode('.jpg', frame)     # _ is use because we don't want to know if encoding suceeded. So, we only care about the 'buffer' which is the JPEG data

    # 'buffer' is now a numpy array but containing JPEG file bytes inside. So, we use .tobytes() , to remove the wrapper containing metadata wrapping the data. Because browser only wants the data (raw byte data with no wrapper)
    # Response is a flask's class for creating HTTP response object. It takes the raw data(bytes) and adds with HTTP headers and proper HTTP response object automatically
    return Response(buffer.tobytes(), mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)