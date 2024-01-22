import cv2




img = cv2.imread("C:\\Users\\Aidan\\Documents\\Projects\\CNC Welding Table\\CNCWelderCode\\computervisioncontrolledcncweldingmachine\\images\\othersideofplate.jpg")
img2 = cv2.imread("C:\\Users\\Aidan\\Documents\\Projects\\CNC Welding Table\\CNCWelderCode\\computervisioncontrolledcncweldingmachine\\images\\othersideofplate.jpg")
combine = cv2.compare(img,img2,cv2.CMP_EQ)
cv2.imshow("Display Image", combine)
cv2.waitKey(0)
cv2.destroyAllWindows()

