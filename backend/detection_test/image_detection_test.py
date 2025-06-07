import cv2
from ultralytics import YOLO
from functions.lpr_help_func import data_province, get_thai_character

source_image = 'MyPhoto/test2.jpg'

plate_detection_model = YOLO('model/license_plate.pt')      # Read license plate from the images or video
read_data_model = YOLO('model/data_plate.pt')                  # Read info inside license plate


def read_license_info(source_path):

    plate_detection_model = YOLO('model/license_plate.pt')      # Read license plate from the images or video
    read_data_model = YOLO('model/data_plate.pt')                  # Read info inside license plate

    source = cv2.imread(source_path)

    detected_class = []
    license_no = ''
    province_name = ''

# Get the result from detecting License plate
    plate_detection_results = plate_detection_model(source, conf=0.4, verbose=False)
    
    for pd_result in plate_detection_results:

        # For each license plate detected (expecting to get only one)
        for plate_box in pd_result.boxes:

            print(plate_box.xyxy)

            # Map the float to int
            x1,y1,x2,y2 = map(int,plate_box.xyxy[0])  # Put 0 to get inside the inside list. Because without [0], it is a nested list
            cv2.rectangle(source,(x1,y1),(x2,y2),(0,255,0),1) # No need to draw in real usecase
        
            # Crop the image on region of interest
            license_roi = source[y1:y2,x1:x2]


            # Detect License info from the license plate roi
            read_detection_results = read_data_model(license_roi,conf=0.4, verbose=False)

            # Keep the plates coordinates in the plate list
            plates = []

            # Get all the coordinates detected from license plate roi and keep it in "plates" list
            for rd_result in read_detection_results:
                for plate_data_box in rd_result.boxes:
                    
                    px1,py1,px2,py2 = map(int,plate_data_box.xyxy[0])

                    

                    # Map the coordiante from cropped image detection to the 'source' image
                    # x1,y1 is the coordinate from the left-side edge to the most left. So, to find the actual coordinate for each data, just add detected px1 with x1
                    px1, px2 = px1+x1 , px2+x1
                    py1, py2 = py1+y1 , py2+y1

                    plates.append((px1, plate_data_box.cls,(px1,px2,py1,py2)))


            # Sort the position of the detected object (letter or province) to the coorect order of actual license plate

            plates.sort(key= lambda x:x[0]) # Sort using the px1 of each object. Where x will be the tuple for each item in the list. And x[0] will return the first item of that tuple for .sort() to work on

            # Collect the detected class ids to class name
            for plate in plates:
                px1,plate_cls_id,(px1,px2,py1,py2) = plate
                
                # Draw rectangle
                cv2.rectangle(source,(px1,py1),(px2,py2),(255,0,0),1)
                
                # Convert plate_cls_id to actual plate detected class name (read_data_model.names is the dictionary containing the detected class ids as a "key" and its name as a "value")
                plate_cls_name = read_data_model.names[int(plate_cls_id)]
                detected_class.append(plate_cls_name)

    if detected_class:
        # Split province class name to the back (for ordering)
        for detect in detected_class:
            if detect in data_province:
                detected_class.remove(detect)       # Remove it first
                detected_class.append(detect)       # Then, add it back to the end
        # print("New Detected Class: ",detected_class)

        
        # Convert the class name(code) to actual name (either license no. or province name)
        combined_text = ""
        for code in detected_class:

            # and Split license no. and province name to different variable
            if code == detected_class[len(detected_class)-1]:
                license_no = combined_text                  # Last combined text before adding the province name
                province_name = get_thai_character(code)    # The province name that will be later added to the combined text

            combined_text += get_thai_character(code)


        print("License No: ",license_no)
        print("Province Name: ", province_name)      

    else:
        print("No license plate detected in this frame")

    cv2.imshow("Result", source)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    

read_license_info(source_image)