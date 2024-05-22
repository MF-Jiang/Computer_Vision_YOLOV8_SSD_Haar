from utils import FPS
import numpy as np
import argparse
import dlib
import cv2
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", type=str, default="./mobilenet_ssd/MobileNetSSD_deploy.prototxt",
                help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", type=str, default="./mobilenet_ssd/MobileNetSSD_deploy.caffemodel",
                help="path to Caffe pre-trained model")
ap.add_argument("-v", "--video", required=True,
                help="path to input video file")
ap.add_argument("-o", "--output", type=str, default="./Result/Sample1.mp4",
                help="path to optional output video file")
ap.add_argument("-c", "--confidence", type=float, default=0.1,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
print("[INFO] starting video stream...")
vs = cv2.VideoCapture(args["video"])
writer = None
trackers = []
labels = []
fps = FPS().start()
tracks = [[] for _ in range(len(trackers))]
while True:
    (grabbed, frame) = vs.read()
    if frame is None:
        break
    (h, w) = frame.shape[:2]
    width = 600
    r = width / float(w)
    dim = (width, int(h * r))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if args["output"] is not None and writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(args["output"], fourcc, 30,
                                 (frame.shape[1], frame.shape[0]), True)
    if len(trackers) == 0:
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (w, h), 127.5)
        net.setInput(blob)
        detections = net.forward()
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > args["confidence"]:
                # extract the index of the class label from the
                # detections list
                idx = int(detections[0, 0, i, 1])
                label = CLASSES[idx]
                if CLASSES[idx] != "person":
                    continue
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                t = dlib.correlation_tracker()
                rect = dlib.rectangle(int(startX), int(startY), int(endX), int(endY))
                t.start_track(rgb, rect)
                labels.append(label)
                trackers.append(t)
                tracks.append([(startX, startY, endX, endY)])
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 255, 0), 2)
                cv2.putText(frame, label, (startX, startY - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
    else:
        for i, (t, l) in enumerate(zip(trackers, labels)):
            tracking_quality = t.update(rgb)
            if tracking_quality < 7:
                del trackers[i]
                del labels[i]
                del tracks[i]
                continue
            pos = t.get_position()
            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          (0, 255, 0), 2)
            cv2.putText(frame, l, (startX, startY - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
            tracks[i].append((startX, startY, endX, endY))
    for track in tracks:
        for i in range(1, len(track)):
            if len(track) > 10:
                cur_center = ((track[i][0] + track[i][2]) // 2, (track[i][1] + track[i][3]) // 2)
                prev_center = ((track[i - 1][0] + track[i - 1][2]) // 2, (track[i - 1][1] + track[i - 1][3]) // 2)
                cv2.line(frame, cur_center, prev_center, (255, 0, 0), 2)
    if writer is not None:
        writer.write(frame)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    fps.update()
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

if writer is not None:
    writer.release()

cv2.destroyAllWindows()
vs.release()
