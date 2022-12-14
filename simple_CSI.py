import cv2
import time
import numpy as np
""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=480,
    display_height=270,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_base_camera():
    window_title = "CSI Camera"

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        cur_timer = 0   #un used atm
        timer = 300
        new_frame_time = 0
        prev_frame_time = 0
        frame_count = 0
        avg_count = 0
        avg_fps = 0
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

            while True:
                cur_timer +=1   #un used atm


                frame_count += 1
                
                new_frame_time = time.time()
                fps2 = 1/(new_frame_time - prev_frame_time)
                fps2 = int(fps2)
                avg_count += fps2
                if frame_count >= 8:
                    avg_fps = avg_count/frame_count
                    avg_fps = int(avg_fps)
                    frame_count = 0 
                    avg_count = 0


               
                prev_frame_time = new_frame_time
                ret_val, frame = video_capture.read()
                fps1 = video_capture.get(cv2.CAP_PROP_FPS)
              
                
               
                #print("fps2: ", fps2)
                print("cur_timer: ", cur_timer)
                print("fps:", avg_fps )
                cv2.putText(frame, f'FPS_expected: {int(fps1)}', (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cv2.putText(frame, f'FPS_actual: {fps2}', (20,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cv2.putText(frame, f'FPS_avg: {avg_fps}', (20,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)



                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                #if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                cv2.imshow(window_title, frame)
                  

                if cur_timer >= timer:
                    break
                keyCode = cv2.waitKey(10) & 0xFF
                 #Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break 
    
                
                
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")

def get_frame(result_id, img_id):
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    #still working on this, does nothing atm


if __name__ == "__main__":
    show_base_camera()