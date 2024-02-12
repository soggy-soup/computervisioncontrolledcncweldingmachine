# code from:https://medium.com/@ed.twomey1/using-charuco-boards-in-opencv-237d8bc9e40d
import os
import numpy as np
import cv2
import glob

# ENTER YOUR PARAMETERS HERE:
ARUCO_DICT = cv2.aruco.DICT_6X6_250
SQUARES_VERTICALLY = 9
SQUARES_HORIZONTALLY = 7
SQUARE_LENGTH = 0.03
MARKER_LENGTH = 0.015
LENGTH_PX = 1080  # total length of the page in pixels
MARGIN_PX = 5    # size of the margin in pixels
SAVE_NAME = 'ChArUco_Marker.png'

PATH_TO_YOUR_IMAGES = 'calibration\\charuco_images'

def img_show(img_to_show):
        aspect_ratio = img_to_show.shape[1] / img_to_show.shape[0]
        cv2.namedWindow("Display Image", cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.imshow("Display Image", img_to_show)

        while True:
            key = cv2.waitKey(1)
            if key == 27:
                break

            current_width = cv2.getWindowImageRect("Display Image")[2]
            new_height = int(current_width / aspect_ratio)
            cv2.resizeWindow("Display Image", current_width, new_height)
        cv2.destroyAllWindows()
        
def calibrate_and_save_parameters():
    # Define the aruco dictionary and charuco board
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv2.aruco.CharucoBoard((SQUARES_VERTICALLY, SQUARES_HORIZONTALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    params = cv2.aruco.DetectorParameters()

    # Load PNG images from folder
    image_files = [os.path.join(PATH_TO_YOUR_IMAGES, f) for f in os.listdir(PATH_TO_YOUR_IMAGES) if f.endswith(".jpg")]
    image_files.sort()  # Ensure files are in order

    all_charuco_corners = []
    all_charuco_ids = []

    for image_file in image_files:
        image = cv2.imread(image_file)
        image_copy = image.copy()
        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(image, dictionary, parameters=params)
        
        # If at least one marker is detected
        if len(marker_ids) > 0:
            cv2.aruco.drawDetectedMarkers(image_copy, marker_corners, marker_ids)
            charuco_retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, image, board)
            if charuco_retval:
                all_charuco_corners.append(charuco_corners)
                all_charuco_ids.append(charuco_ids)

    # Calibrate camera
    retval, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(all_charuco_corners, all_charuco_ids, board, image.shape[:2], None, None)

    # Save calibration data
    np.save('calibration\\14%_camera_matrix.npy', camera_matrix)
    np.save('calibration\\14%_dist_coeffs.npy', dist_coeffs)

    # Iterate through displaying all the images
    '''
    for image_file in image_files:
        image = cv2.imread(image_file)
        undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs)
        img_show(undistorted_image)
    '''

def create_and_save_new_board():
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv2.aruco.CharucoBoard((SQUARES_VERTICALLY, SQUARES_HORIZONTALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    size_ratio = SQUARES_HORIZONTALLY / SQUARES_VERTICALLY
    img = cv2.aruco.CharucoBoard.generateImage(board, (LENGTH_PX, int(LENGTH_PX*size_ratio)), marginSize=MARGIN_PX)
    cv2.imshow("img", img)
    cv2.waitKey(2000)
    cv2.imwrite(SAVE_NAME, img)

def detect_pose(image, camera_matrix, dist_coeffs):
    # Undistort the image
    undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs,None,None)

    # Define the aruco dictionary and charuco board
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    board = cv2.aruco.CharucoBoard((SQUARES_VERTICALLY, SQUARES_HORIZONTALLY), SQUARE_LENGTH, MARKER_LENGTH, dictionary)
    params = cv2.aruco.DetectorParameters()

    # Detect markers in the undistorted image
    marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(undistorted_image, dictionary, parameters=params)
    
    # If at least one marker is detected
    if len(marker_ids) > 0:
        # Interpolate CharUco corners
        charuco_retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(marker_corners, marker_ids, undistorted_image, board)

        # If enough corners are found, estimate the pose
        if charuco_retval:
            retval, rvec, tvec = cv2.aruco.estimatePoseCharucoBoard(charuco_corners, charuco_ids, board, camera_matrix, dist_coeffs, None, None)

            # If pose estimation is successful, draw the axis
            if retval:
                cv2.drawFrameAxes(undistorted_image, camera_matrix, dist_coeffs, rvec, tvec, length=0.1, thickness=15)
    return undistorted_image

def main():
    # Load calibration data
    camera_matrix = np.load('calibration\\14%_camera_matrix.npy')
    dist_coeffs = np.load('calibration\\14%_dist_coeffs.npy')
    
    # Iterate through PNG images in the folder
    image_files = glob.glob("calibration\\charuco_images\\*.jpg")
    
    for image_file in image_files:
        # Load an image
        image = cv2.imread(image_file)
        
        # Detect pose and draw axis
        pose_image = detect_pose(image, camera_matrix, dist_coeffs)

        # Show the image
        img_show(pose_image)
        #cv2.imshow('Pose Image', pose_image)
        #cv2.waitKey(0)

#create_and_save_new_board()

calibrate_and_save_parameters()

main()