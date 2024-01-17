import cv2

def live_video_show():
    cap = cv2.VideoCapture(0, cv2.CAP_MSMF)  # Change 0 to the index of your camera if not the default

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        return

    aspect_ratio = frame.shape[1] / frame.shape[0]

    cv2.namedWindow("Live Video", cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
    cv2.imshow("Live Video", frame)

    while True:
        key = cv2.waitKey(1)
        if key == 27:  # Break the loop if 'Esc' key is pressed
            break

        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        current_width = cv2.getWindowImageRect("Live Video")[2]
        new_height = int(current_width / aspect_ratio)
        cv2.resizeWindow("Live Video", current_width, new_height)
        cv2.imshow("Live Video", frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    live_video_show()



'''
# open video0
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
# set width and height
# MJPG 10fps@4656x3496/3840x2160/2592x1944;
# 30fps@2320x1744/1920x1080/1600x1200/1280x720/800x600/640x480/320x240 
# YUV 5fps@1600x1200; 
# YUV 10fps@1280x720; 
# YUV 15fps@800x600; 
# YUV 20fps@640x480/320x240
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4656)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3496)
# set fps
cap.set(cv2.CAP_PROP_FPS, 10)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    scaled_frame = scalevideo(frame, percent = 50)
    # Display the resulting frame
    cv2.imshow('newframe', scaled_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
'''