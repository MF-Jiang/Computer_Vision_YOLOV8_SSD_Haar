import cv2
import tkinter as tk
from tkinter import filedialog


def video_test():
    root = tk.Tk()
    root.withdraw()

    return filedialog.askopenfilename()


def haar_detection():
    face_path = 'haarcascades\\haarcascade_frontalface_default.xml'
    eye_path = 'haarcascades\\haarcascade_eye.xml'
    smile_path = 'haarcascades\\haarcascade_smile.xml'
    diction = {'face': face_path, 'eye': eye_path, 'smile': smile_path}
    for i in diction:
        diction[i] = cv2.CascadeClassifier(diction[i])
    return diction


def video_detection(video_file, detection):
    video_capture = cv2.VideoCapture(video_file)
    if not video_capture.isOpened():
        print("Error: Could not open video file ", video_file)
        exit()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_ret = detection['face'].detectMultiScale(gray_frame, scaleFactor=1.02, minNeighbors=5, minSize=(15, 15),
                                                      maxSize=(50, 50), flags=cv2.CASCADE_DO_CANNY_PRUNING)
        for (x, y, w, h) in face_ret:
            face_roi = gray_frame[y:y + h, x:x + w]
            eye_ret = detection['eye'].detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=3, minSize=(15, 15),
                                                        flags=cv2.CASCADE_SCALE_IMAGE)
            smile_ret = detection['smile'].detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=3, minSize=(15, 15),
                                                            flags=cv2.CASCADE_SCALE_IMAGE)
            for (xx, yy, ww, hh) in eye_ret:
                pt1 = (x + xx, y + yy)
                pt2 = (pt1[0] + ww, pt1[1] + hh)
                cv2.rectangle(frame, pt1, pt2, (255, 0, 0), 2)
            for (xx, yy, ww, hh) in smile_ret:
                pt1 = (x + xx, y + yy)
                pt2 = (pt1[0] + ww, pt1[1] + hh)
                cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_file = video_test()
    detector = haar_detection()
    video_detection(video_file, detector)
