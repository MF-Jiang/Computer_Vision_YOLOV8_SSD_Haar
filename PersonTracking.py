import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import variables
from collections import defaultdict
from ultralytics import YOLO


def Person_Tracking(root, args, select_button, widthShow, heightShow):
    # Loading the model
    model = YOLO('./model_yolo/yolov8n.pt', verbose=False)
    models = YOLO('./model_yolo/yolov8s.pt', verbose=False)

    # Open video file
    video_path = args["video"]
    variables.cap = cv2.VideoCapture(video_path)

    # Store trace history
    track_history = defaultdict(lambda: [])

    # Defines the codec and frame rate for the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = variables.cap.get(cv2.CAP_PROP_FPS)
    width = int(variables.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(variables.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create an output video file
    output_video_path = args["output"]
    variables.out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    variables.Processing = True
    # Whether to pause the video
    variables.Video_Playing = True

    Exit = False

    # Create a Tkinter window
    tk_frame = tk.Frame(root)
    tk_frame.pack(side='left', padx=20, pady=40, anchor='nw')
    # tk_frame.pack()
    # Create a Tkinter Label to display video frames
    label = tk.Label(tk_frame)
    label.pack(side='left', padx=20, pady=40, anchor='nw')
    # label.pack()
    # Loop over video frames
    while variables.cap.isOpened() and Exit is False and variables.END is False:
        # If the video pauses, wait until it resumes
        # while variables.Video_Playing is False:
        #     pass
        # Read a frame from the video
        success, current_frame = variables.cap.read()

        if success:
            # Run YOLOv8 tracking on frames to continuously track objects between frames
            results1 = model.track(current_frame, persist=True)
            results2 = models.track(current_frame, persist=True)
            # Ensemble model results
            results = results1 + results2

            if results and results[0].boxes:  # Check whether the result is empty

                if variables.multiple is False and len(results[0].boxes) > 1:
                    results[0].boxes = results[0].boxes[:1]

                # Gets the box and trace ID
                boxes = results[0].boxes.xywh.cpu()
                try:
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                    class_ids = results[0].boxes.cls.int().cpu().tolist()  # Get category information for the box

                    # Draw the tracing path and detection box
                    for box, track_id, class_id in zip(boxes, track_ids, class_ids):
                        if class_id == 0:  # The ID of the "person" class is usually 0, which you can determine based
                            # on the class index of the YOLO model
                            x, y, w, h = box
                            track = track_history[track_id]
                            track.append((float(x), float(y)))  # x, y center point

                            # Draw a trace
                            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))

                            if variables.Tracking:
                                if variables.path:
                                    cv2.polylines(current_frame, [points], isClosed=False, color=(230, 230, 230),
                                                  thickness=10)

                                # Draw the detection box
                                cv2.rectangle(current_frame, (int(x - w / 2), int(y - h / 2)),
                                              (int(x + w / 2), int(y + h / 2)),
                                              (0, 255, 0), 2)
                except:
                    pass

            # Write the annotated frames to the output video file
            variables.out.write(current_frame)

            # Convert OpenCV frames to PIL images and resize to fit the window
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(current_frame)
            pil_img = pil_img.resize((widthShow, heightShow), Image.ANTIALIAS)  # Resize to fit the window
            tk_img = ImageTk.PhotoImage(image=pil_img)

            # update the image in the Label
            label.configure(image=tk_img)
            label.image = tk_img

            # update the Tkinter window
            root.update()

        else:
            # Exit the loop if the video ends
            break

    # Release the video capture object, output the video object and close the display window
    label.image = None
    variables.cap.release()
    variables.out.release()
    variables.Video_Playing = False
    variables.Processing = False

    cv2.destroyAllWindows()


