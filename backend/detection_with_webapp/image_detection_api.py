from flask import Flask, Response,jsonify, request, send_file
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
import time
import io

from functions.lpr_help_func import data_province, get_thai_character


app = Flask(__name__)
CORS(app)


frame_path = 'MyPhoto/test4.jpg'
# source_path = 'MyVideo/video1.MOV'

# License No. and Province name detected
license_no = ""
province_name = ""

def detect_image(frame_path):
    
    # Initialize associated variables
    detected_class = []
    global license_no, province_name

    # Resest the variable to empty
    license_no = ""
    province_name = ""

    # Initialize Models
    plate_detection_model = YOLO("model/license_plate.pt")
    read_data_model = YOLO("model/data_plate.pt")

    frame = cv2.imread(frame_path)

    ## Find License Plate with plate_detection_model first

    # Get the result of the model detected
    plate_detection_results = plate_detection_model(frame, conf=0.4, verbose=False)

    # Get into the object inside the list (plate_detection_result) using for loop to get the first index which is the object we need containing 'boxes'
    for pd_result in plate_detection_results:

        # Get the attributes we want from the 'boxes key in the result object'
        for plate_box in pd_result.boxes:

            # Get the coordinate of the license plate detected
            x1,y1,x2,y2 = map(int,plate_box.xyxy[0])    # Add [0] to get inside the nested list (because we want the inner list)

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

            # Crop the detected frame or region of interest
            license_roi = frame[y1:y2,x1:x2]


            # Now, detect the license data inside license_roi
            read_data_model_results = read_data_model(license_roi, conf=0.4,verbose=False)

            # Get into the object desired from a list by loop to first index
            plates = []
            for rd_result in read_data_model_results:
                
                # Get attributes from each detected object in "boxes"
                for plate_data_box in rd_result.boxes:
                    
                    # Get coordinate detected of each object
                    px1,py1,px2,py2 = map(int,plate_data_box.xyxy[0])

                    # Map the coordinate of the cropped frame to the original frame
                    px1,px2 = px1+x1 , px2+x1
                    py1,py2 = py1+y1 , py2+y1

                    plates.append((px1,plate_data_box.cls,(px1,py1,px2,py2)))

                
            # Sort the plate_data detected to be in order from left to right
            plates.sort(key=lambda x:x[0]) # x is the plates[] item inside plates. Where we want x[0] which is the first index of each item in plates or "px1" 
            
            # Destruct the plates list
            detected_class = []
            for plate in plates:
                
                px1,plate_cls_id,(px1,py1,px2,py2) = plate

                cv2.rectangle(frame,(px1,py1),(px2,py2),(255,0,0),2)

                # Get the class name from the class_id using "read_data_model.names" which is a dictionary containing class_id and class_name
                plate_cls_name = read_data_model.names[int(plate_cls_id)]
                detected_class.append(plate_cls_name)

            if detected_class:

                # Move the province name to the back
                for detect in detected_class:
                    if detect in data_province:
                        detected_class.remove(detect)   # Remove the province class name
                        detected_class.append(detect)   # Append it back to the last index


                # Get the actual name out of the class_name (just a label name). Actual name will be the full name listed in dictionary
                combined_text = ""
                for class_name in detected_class:
                    
                    # Split between license no. and province name
                    if class_name == detected_class[len(detected_class)-1]:
                        license_no = combined_text                          # Last combined_text before adding the province name (last index of detected_class)
                        province_name = get_thai_character(class_name)      # Province name is the last index of detected_class
                    
                    combined_text += get_thai_character(class_name)


                print("Check no:",license_no)
                print("Check prov:",province_name)

            else:
                # Clear variable when it does not detected
                license_no = 'No. Not detected'
                province_name = 'Prov Not detected'

    return frame



### API ENDPOINT


@app.route('/get_image')
def get_image():
     
    # Call the function to detect the image
    detected_frame = detect_image(frame_path)

    # Image encoding (compress raw pixel data into JPEG format)
        # Input:    Raw numpy array
        # Output:   Tuple of (success_flag, encoded_bytes)
    _, buffer = cv2.imencode('.jpg', detected_frame)     # _ is use because we don't want to know if encoding suceeded. So, we only care about the 'buffer' which is the JPEG data

    # 'buffer' is now a numpy array but containing JPEG file bytes inside. So, we use .tobytes() , to remove the wrapper containing metadata wrapping the data. Because browser only wants the data (raw byte data with no wrapper)
    # Response is a flask's class for creating HTTP response object. It takes the raw data(bytes) and adds with HTTP headers and proper HTTP response object automatically
    return Response(buffer.tobytes(), mimetype='image/jpeg')


@app.route('/get_license_data')
def get_data():

    license_data = {
        "license_no" : license_no,
        "province_name" : province_name
    }

    print(license_data)

    return(jsonify(license_data))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)