from tkinter import filedialog
from tkinter import simpledialog
import tkinter as tk
import cv2
import os
import subprocess
import variables
from PersonTracking import Person_Tracking


# Click the select button on the UI, note that you want to clear the cache data, pass in the components that can't be
# deleted, and delete everything else
def select_video(root, args, select_button, result_button, output_button, size_button, quitv_button, tracking_button,
                 close_button, frame1, multiple_button, path_button):
    if variables.cap is not None:
        variables.cap.release()
    if variables.out is not None:
        variables.out.release()
    cv2.destroyAllWindows()
    # reset the state variable
    variables.Processing = False
    variables.Video_Playing = True  # Set the video to play on restart
    variables.END = False  # reset the end flag
    root.update()
    for widget in root.winfo_children():
        if widget not in [select_button, result_button, output_button, size_button, quitv_button, tracking_button,
                          close_button, frame1, multiple_button, path_button]:
            widget.destroy()

    file_path = filedialog.askopenfilename()
    if file_path:
        args["video"] = file_path
        Person_Tracking(root, args, select_button, args["width"], args["height"])
        Quit_Video(root, select_button, result_button, output_button, size_button, quitv_button, tracking_button,
                   close_button, frame1, multiple_button, path_button)


# Pause and resume playback. This was done, but it was deprecated because the thread could not
# be present in the PersonTracking function, which would have resulted in deadlock resolution.
def Pause_or_Play():
    print(variables.Video_Playing)
    variables.Video_Playing = not variables.Video_Playing


# Check the update button status.
def check_processing_status(select_button, output_button, size_button, quitv_button, tracking_button, multiple_button,
                            path_button):
    if variables.Processing:
        output_button.config(state=tk.DISABLED)
        size_button.config(state=tk.DISABLED)
        quitv_button.config(state=tk.NORMAL)
        tracking_button.config(state=tk.NORMAL)
        multiple_button.config(state=tk.NORMAL)
        path_button.config(state=tk.NORMAL)
        if variables.Tracking:
            tracking_button.config(text="Untracking")
        else:
            tracking_button.config(text="Start Tracking")
        if variables.multiple:
            multiple_button.config(text="Multiple Tracking")
        else:
            multiple_button.config(text="Single Tracking")
        if variables.path:
            path_button.config(text="Showing Route")
        else:
            path_button.config(text="Hding Route")
    else:
        output_button.config(state=tk.NORMAL)
        size_button.config(state=tk.NORMAL)
        quitv_button.config(state=tk.DISABLED)
        tracking_button.config(state=tk.DISABLED)
        tracking_button.config(text="Tracking")
        multiple_button.config(state=tk.DISABLED)
        multiple_button.config(text="Multiple/Single")
        path_button.config(state=tk.DISABLED)
        path_button.config(text="Route Button")

    if variables.Tracking:
        multiple_button.config(state=tk.NORMAL)
        path_button.config(state=tk.NORMAL)
    else:
        multiple_button.config(state=tk.DISABLED)
        path_button.config(state=tk.DISABLED)

    if not variables.END:
        select_button.after(1000, check_processing_status, select_button, output_button, size_button, quitv_button,
                            tracking_button, multiple_button, path_button)


# Close and clear all data
def on_closing(root):
    root.quit()
    variables.END = True

    if variables.cap is not None:
        variables.cap.release()
    if variables.out is not None:
        variables.out.release()
    cv2.destroyAllWindows()
    root.destroy()


# Open the output folder function
def open_result_folder():
    result_folder_path = ".\Result"
    if os.path.exists(result_folder_path):
        subprocess.Popen(["explorer", result_folder_path])
    else:
        print("Result folder does not exist.")


# Change the output filename
def get_output_filename(args):
    filename = simpledialog.askstring("Enter Output Filename", "Enter the filename for the output video:")
    if filename:
        args["output"] = f"./Result/{filename}.mp4"
    else:
        return None


# Setting the video size
def get_dimensions(args):
    width = simpledialog.askinteger("Input", "Enter width:")
    height = simpledialog.askinteger("Input", "Enter height:")
    if width and height:
        args["width"] = width
        args["height"] = height
    else:
        return


# Close the video
def Quit_Video(root, select_button, result_button, output_button, size_button, quitv_button, close_button,
               tracking_button, frame1, multiple_button, path_button):
    if variables.Processing:
        if variables.cap is not None:
            variables.cap.release()
        if variables.out is not None:
            variables.out.release()
        cv2.destroyAllWindows()

        variables.Processing = False
        variables.Video_Playing = True
        variables.END = False
        root.update()

        for widget in root.winfo_children():
            if widget not in [select_button, result_button, output_button, size_button, quitv_button, tracking_button,
                              close_button, frame1, multiple_button, path_button]:
                widget.destroy()


# Switching Tracking
def tracking_Start():
    variables.Tracking = not variables.Tracking


# Switching multiple or single
def multiple_or_single():
    variables.multiple = not variables.multiple


# Toggle whether to draw a route
def path_start():
    variables.path = not variables.path
