import tkinter as tk
import argparse

from UI import select_video, get_output_filename, get_dimensions, open_result_folder, tracking_Start, Quit_Video, \
    on_closing, check_processing_status, multiple_or_single, path_start


def main():
    # Setting passed parameters
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=False,
                    help="path to input video file")
    ap.add_argument("-o", "--output", type=str, default="./Result/Sample0.mp4",
                    help="path to optional output video file")
    ap.add_argument("-w", "--width", type=float, default=540, help="displays the width of the video")
    ap.add_argument("-H", "--height", type=float, default=360, help="displays the height of the video")
    args = vars(ap.parse_args())

    # Creating a window
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.title("Computer Vision CourseWork")
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # Building screen components
    frame1 = tk.Frame(root)
    frame1.pack(side='top', pady=20)

    # Set buttons
    select_button = tk.Button(frame1, text="Select Video",
                              command=lambda: select_video(root, args, select_button, result_button, output_button,
                                                           size_button, quitv_button, tracking_button, close_button,
                                                           frame1, multiple_button, path_button))
    select_button.pack(side='left', padx=20)

    output_button = tk.Button(frame1, text="Output Filename", command=lambda: get_output_filename(args))
    output_button.pack(side='left', padx=20)

    size_button = tk.Button(frame1, text="Size Set", command=lambda: get_dimensions(args))
    size_button.pack(side='left', padx=20)

    result_button = tk.Button(frame1, text="Open Result Folder", command=open_result_folder)
    result_button.pack(side='left', padx=20)

    tracking_button = tk.Button(frame1, text="Track Button", command=tracking_Start)
    tracking_button.pack(side='left', padx=20)

    path_button = tk.Button(frame1, text="Route Button", command=path_start)
    path_button.pack(side='left', padx=20)

    multiple_button = tk.Button(frame1, text="Multiple/Single", command=multiple_or_single)
    multiple_button.pack(side='left', padx=20)

    quitv_button = tk.Button(frame1, text="Quit Video",
                             command=lambda: Quit_Video(root, select_button, result_button, output_button, size_button,
                                                        quitv_button, close_button, tracking_button, frame1,
                                                        multiple_button, path_button))
    quitv_button.pack(side='left', padx=20)

    close_button = tk.Button(frame1, text="Quit Program", command=lambda: on_closing(root))
    close_button.pack(side='left', padx=20)

    # Update button state
    check_processing_status(select_button, output_button, size_button, quitv_button, tracking_button, multiple_button,
                            path_button)

    root.mainloop()


if __name__ == "__main__":
    main()
