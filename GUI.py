from tkinter import *
from PIL import Image, ImageTk
import cv2


cap = cv2.VideoCapture(0)
width, height = 100,100
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 


app = Tk()
#app.geometry("700x450")
app.bind('<Escape>', lambda e: app.quit())

video_stream = Label(app)
video_stream.pack()



def open_camera():
    _, frame = cap.read()
    cv2_img =  cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cap_img = Image.fromarray(cv2_img)
    photo_img = ImageTk.PhotoImage(image = cap_img)
    video_stream.photo_img = photo_img
    video_stream.configure(image =photo_img)
    video_stream.after(10,open_camera)
    
open_camera()   
b1 = Button(app, text = "Stream", command = None)
b1.pack(side = RIGHT)

app.mainloop()

