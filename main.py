from flask import Flask, render_template, Response
import cv2
import numpy as np
import os
from config import RTSP_URL, YOLO_WEIGHTS, YOLO_CFG, COCO_NAMES

app = Flask(__name__)

# Load YOLO
net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
layer_names = net.getLayerNames()
unconnected_out_layers = net.getUnconnectedOutLayers()
output_layers = [layer_names[i - 1] for i in unconnected_out_layers.flatten()]

# Load COCO names
with open(COCO_NAMES, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Counter for snapshot filenames
snapshot_counter = 0

@app.route('/')
def index():
    return render_template('index.html')

def save_snapshot(frame):
    global snapshot_counter
    snapshot_folder = 'snapshots'
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)
    snapshot_path = os.path.join(snapshot_folder, f'snapshot_{snapshot_counter}.jpg')
    cv2.imwrite(snapshot_path, frame)
    snapshot_counter += 1
    print(f"Snapshot saved: {snapshot_path}")

def detect_cats():
    cap = cv2.VideoCapture(RTSP_URL)

    if not cap.isOpened():
        print("Error: Couldn't open video stream.")
        return None

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't read frame.")
            break

        height, width, channels = frame.shape

        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        cat_detected = False

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6 and classes[class_id] == "cat":
                    cat_detected = True
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, 'Cat', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                if cat_detected:
                    save_snapshot(frame)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(detect_cats(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
