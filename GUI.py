from tkinter import *
from PIL import Image, ImageTk
import cv2

import customtkinter
import numpy as np
import weld_joint
import grbl_gcode
import util_funcs.displayimg


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        #initialize window properties
        self.bind('<Escape>', lambda e: self.quit())
        self.title("CNC Welder")
        self.resizable(width=False, height=False)
        #customtkinter.set_appearance_mode("dark")
        
        #setup video stream with opencv      
        self.cap = cv2.VideoCapture(0,cv2.CAP_MSMF)
        video_width, video_height = 1280,720
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, video_width) 
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height) 
        focus = 100
        self.cap.set(28,focus)
        video_aspect_ratio = video_width/video_height
        self.video_win_width, self.video_win_height = 800, int(800/video_aspect_ratio)
        tot_rows = 15
        
        #initialize contours as empty
        self.contours1 = None
        self.contours2 = None
        self.joint_intersection = None
        
        #switch states to ensure first picture is taken before second
        self.img12pressed = True
        self.img1_state = NORMAL
        self.img2_state = DISABLED
        
        
        #create video stream label
        self.video_stream = customtkinter.CTkLabel(self,text="")
        self.video_stream.grid(row=0,column=0, padx=10,pady=10,rowspan=tot_rows)
        
        #frame for all buttons
        right_frame = customtkinter.CTkFrame(self, width=600, height=self.video_win_height).grid(row=0,column=1,padx=10,pady=10,columnspan=3,rowspan=tot_rows)

        #setup buttons
        customtkinter.CTkLabel(self, text="Setup:").grid(row=0,column=1,ipadx=5)
        self.zoompercent = DoubleVar()
        cam_zoom_btn = customtkinter.CTkButton(self,text="Set Zoom").grid(row=1,column=1)
        cam_zoom_slider = customtkinter.CTkSlider(self,variable = self.zoompercent,from_=0,to=99,number_of_steps=99,orientation=HORIZONTAL, command = self.disp_zoompercent).grid(row=1,column=2,ipady=5)
        self.zoompercent.set(0)

        #image processing buttons
        customtkinter.CTkLabel(self, text="Joint Detection:").grid(row=2,column=1)
        self.img1 = customtkinter.CTkButton(self,text="Picture 1",fg_color="red",state=self.img1_state, command=self.process_img).grid(row=3,column=1)
        self.img2 = customtkinter.CTkButton(self,text="Picture 2",fg_color="blue",state=self.img2_state,command=self.process_img).grid(row=3,column=2)
        joint_location = customtkinter.CTkButton(self,text="Weld Joint",command = self.joint).grid(row=3,column=3)

        #material/welder setup buttons
        customtkinter.CTkLabel(self, text="Material Setup:").grid(row=5,column=1)
        self.mat_thck = DoubleVar()
        mat_btn = customtkinter.CTkButton(self,text="Set Material Thickness (mm)").grid(row=6,column=1)
        mat_slider = customtkinter.CTkSlider(self,variable = self.mat_thck,from_=0,to=9,number_of_steps=90,orientation=HORIZONTAL,command = self.disp_mat_thck).grid(row=6,column=2,ipady=5)
        self.mat_thck.set(0)

        #gcode/machine control buttons
        customtkinter.CTkLabel(self, text="GCODE:").grid(row=7,column=1)
        customtkinter.CTkButton(self,text="Generate G-Code").grid(row=8,column=1)
        customtkinter.CTkButton(self,text="Execute").grid(row=8,column=2)
        
        
        self.open_camera()
        
    def disp_zoompercent(self,event=None):
        customtkinter.CTkLabel(self,width=40,text=f"{np.round(self.zoompercent.get(),2)}").grid(row=1,column=3,)

    def disp_mat_thck(self, event=None):
        customtkinter.CTkLabel(self,width=40,text=f"{np.round(self.mat_thck.get(),2)}").grid(row=6,column=3)

    def open_camera(self):
        _, self.frame = self.cap.read()
        cv2_img = cv2.drawContours(self.frame, self.contours1, -1, (0,0,255), thickness = 7)
        cv2_img = cv2.drawContours(cv2_img, self.contours2, -1, (0,255,0), thickness = 7)
        cv2_img = cv2.drawContours(cv2_img, self.joint_intersection, -1, (255,0,0), thickness = 7)
        cv2_img =  cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGBA)
        cap_img = Image.fromarray(cv2_img)
        photo_img = customtkinter.CTkImage(light_image=cap_img,size=(self.video_win_width,self.video_win_height))
        self.video_stream.photo_img = photo_img
        self.video_stream.configure(image =photo_img)
        self.video_stream.after(10,self.open_camera)
    
    def process_img(self):
        path = weld_joint.process_img()
        path.img_in_processing = self.frame
        path.img_crop(100,3496,500,3496)
        path.img_bilateral_blur()
        path.img_detect_HSV_contours() 
        path.largest_contour()
        

        if (self.img12pressed==True):
            self.img12pressed = False
            self.img1_state = DISABLED
            self.img2_state = NORMAL
            self.contours2 = None
            self.joint_intersection = None
            self.contours1 = path.contours
        else:
            self.img12pressed = True
            self.img1_state = NORMAL
            self.img2_state = DISABLED
            self.contours2 = path.contours

        self.grid_slaves(row=3, column=1)[0].configure(state=self.img1_state)
        self.grid_slaves(row=3, column=2)[0].configure(state=self.img2_state)
    
    def joint(self):
        if ((self.contours1 is not None) & (self.contours2 is not None)):
            self.joint_intersection = weld_joint.radius_intersect(self.contours1,self.contours2,radius=3)
            self.contours1 = None
            self.contours2 = None
            
         
        



app = App()
app.mainloop()

