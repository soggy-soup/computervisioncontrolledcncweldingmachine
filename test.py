import cv2




img = cv2.imread("images\\orangebackground.jpg")
img2 = cv2.imread("images\\bothpieces.jpg")
img_to_show = cv2.compare(img,img2,cv2.CMP_EQ)
 
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

