import time
import cv2

import numpy as np

from config import YOLO_WEIGHTS, YOLO_CFG, COCO_NAMES, SNAPSHOT_INTERVAL

# Load YOLO
net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)
layer_names = net.getLayerNames()
unconnected_out_layers = net.getUnconnectedOutLayers()
output_layers = [layer_names[i - 1] for i in unconnected_out_layers.flatten()]

# Load COCO names
with open(COCO_NAMES, "r") as f:
    classes = [line.strip() for line in f.readlines()]

last_snapshot_time = 0

def detect_cats(rtsp_url):
    global last_snapshot_time

    cap = cv2.VideoCapture(rtsp_url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    if not cap.isOpened():
        print(f"Error: Couldn't open video stream at {rtsp_url}.")
        return None

    frame_count = 0
    frame_skip = 5  # Process one frame every 5 frames to reduce load

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't read frame.")
            continue

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        try:
            height, width, channels = frame.shape
        except Exception as e:
            print(f"Error processing frame: {e}")
            continue

        # Resize the frame to improve processing speed
        frame_resized = cv2.resize(frame, (320, 320))
        blob = cv2.dnn.blobFromImage(frame_resized, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        current_time = time.time()
        cat_detected = False
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6 and classes[class_id] == "cat":
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    # Draw rectangle around detected object
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # Put label (class name) on the detected object
                    cv2.putText(frame, 'Cat', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Capture and save the snapshot
                    if current_time - last_snapshot_time >= SNAPSHOT_INTERVAL:
                        snapshot_filename = f'snapshots/snapshot_{int(current_time)}.jpg'
                        cv2.imwrite(snapshot_filename, frame)
                        print(f"Snapshot saved to {snapshot_filename}")
                        last_snapshot_time = current_time

                    cat_detected = True
                    break
            if cat_detected:
                break

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
