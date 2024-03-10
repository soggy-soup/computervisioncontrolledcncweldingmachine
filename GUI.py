from tkinter import *
from PIL import Image, ImageTk
import cv2

import customtkinter
import time
import numpy as np
import weld_joint
import grbl_gcode
import util_funcs.displayimg


def showframe(self):
    print(zoompercent.get())
    
    customtkinter.CTkLabel(master=root,width=40,text=f"{np.round(zoompercent.get(),2)}").grid(row=1,column=3,)
    customtkinter.CTkLabel(master=root,width=40,text=f"{np.round(mat_thck.get(),2)}").grid(row=6,column=3)

    

def open_camera():
    _, frame = cap.read()
    cv2_img =  cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    
    cap_img = Image.fromarray(cv2_img)
    photo_img = customtkinter.CTkImage(dark_image=cap_img,size=(video_win_width,video_win_height))
    #photo_img = ImageTk.PhotoImage(image = cap_img)
    video_stream.photo_img = photo_img
    video_stream.configure(image =photo_img)
    video_stream.after(10,open_camera)
    
cap = cv2.VideoCapture(0,cv2.CAP_MSMF)
video_width, video_height = 1280,720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, video_width) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height) 
focus = 100
cap.set(28,focus)

video_aspect_ratio = video_width/video_height
video_win_width, video_win_height = 800, int(800/video_aspect_ratio)
tot_rows = 15


customtkinter.set_appearance_mode("dark")
root = customtkinter.CTk()
root.bind('<Escape>', lambda e: root.quit())
root.title("CNC Welder")
root.resizable(width=False, height=False)

video_stream = customtkinter.CTkLabel(master=root,text="")
video_stream.grid(row=0,column=0, padx=10,pady=10,rowspan=tot_rows)

right_frame = customtkinter.CTkFrame(master=root, width=600, height=video_win_height).grid(row=0,column=1,padx=10,pady=10,columnspan=3,rowspan=tot_rows)

customtkinter.CTkLabel(master=root, text="Setup:").grid(row=0,column=1,ipadx=5)
zoompercent = DoubleVar()
cam_zoom_btn = customtkinter.CTkButton(master=root,text="Set Zoom").grid(row=1,column=1)
cam_zoom_slider = customtkinter.CTkSlider(master=root,variable = zoompercent,from_=0,to=99,number_of_steps=99,orientation=HORIZONTAL, command = showframe).grid(row=1,column=2,ipady=5)
zoompercent.set(0)
#draw_workspace = customtkinter.CTkButton(master=root,text="Draw Workspace").grid(row=1,column=3)

customtkinter.CTkLabel(master=root, text="Joint Detection:").grid(row=2,column=1)
img1 = customtkinter.CTkButton(master=root,text="Picture 1",fg_color="red").grid(row=3,column=1)
img2 = customtkinter.CTkButton(master=root,text="Picture 2",fg_color="blue").grid(row=3,column=2)
joint_location = customtkinter.CTkButton(master=root,text="Weld Joint").grid(row=3,column=3)

customtkinter.CTkLabel(master=root, text="Material Setup:").grid(row=5,column=1)
mat_thck = DoubleVar()
mat_btn = customtkinter.CTkButton(master=root,text="Set Material Thickness (mm)").grid(row=6,column=1)
mat_slider = customtkinter.CTkSlider(master=root,variable = mat_thck,from_=0,to=9,number_of_steps=90,orientation=HORIZONTAL,command = showframe).grid(row=6,column=2,ipady=5)
mat_thck.set(0)

customtkinter.CTkLabel(master=root, text="GCODE:").grid(row=7,column=1)
customtkinter.CTkButton(master=root,text="Generate G-Code").grid(row=8,column=1)
customtkinter.CTkButton(master=root,text="Execute").grid(row=8,column=2)



open_camera()

root.mainloop()

