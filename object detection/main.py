import random

import cv2
import numpy
from ultralytics import YOLO
import serial

ser = serial.Serial(port='COM9', baudrate=115200)

# opening the file in read mode
my_file = open("coco1.txt", "r")
# reading the file
data = my_file.read()
# replacing end splitting the text | when newline ('\n') is seen.
class_list = data.split("\n")
my_file.close()

# for waste classification
bio = [1, 6] # these numbers correspond to to indexes based on coco1.txt
nonbio = [0, 3, 4]
recyc = [2, 5, 7, 8, 9, 10]

# Generate random colors for class list
detection_colors = []
for i in range(len(class_list)):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    detection_colors.append((b, g, r))

# load the trained YOLOv8n model
model = YOLO("best.pt")

# cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #  resize the frame | small frame optimise the run
    frame = cv2.resize(frame, (640, 480))

    # Predict on image
    detect_params = model.predict(source=[frame], conf=0.45, save=False)

    # Convert tensor array to numpy
    DP = detect_params[0].numpy()
    if len(DP) != 0:

            boxes = detect_params[0].boxes
            box = boxes[0]  # returns one box
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]

            cv2.rectangle(
                frame,
                (int(bb[0]), int(bb[1])),
                (int(bb[2]), int(bb[3])),
                detection_colors[int(clsID)],
                3,
            )

            # Display class name and confidence
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(
                frame,
                class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                (int(bb[0]), int(bb[1]) - 10),
                font,
                1,
                (255, 255, 255),
                2,
            )

            if int(clsID) in bio:
                ser.write(b'b')
                print("b")
            elif int(clsID) in nonbio:
                ser.write(b'n')
                print("n")
            elif int(clsID) in recyc:
                ser.write(b'r')
                print("r")
            else:
                ser.write(b'off')
                print("off")

    # Display the resulting frame
    cv2.imshow("ObjectDetection", frame)

    # Terminate run when "Q" pressed 
    if cv2.waitKey(1) == ord("q"):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
