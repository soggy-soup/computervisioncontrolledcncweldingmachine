from tkinter import *
from PIL import Image, ImageTk
import cv2
import customtkinter
import numpy as np
import weld_joint
import grbl_gcode

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Initialize window properties
        self.bind('<Escape>', lambda e: self.quit())
        self.title("CNC Welder")
        self.resizable(width=False, height=False)
        customtkinter.set_appearance_mode("dark")

        # Setup video stream with OpenCV
        self.cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(28, 100)
        tot_rows = 15

        # Initialize contours as empty
        self.contours1 = None
        self.contours2 = None
        self.joint_intersection = None
        self.path_wrt_aruco = None
        self.corners = None

        # Switch states to ensure the first picture is taken before the second
        self.img1_state = NORMAL
        self.img2_state = DISABLED
        self.intersection_state = DISABLED

        # Create video stream label
        self.video_stream = customtkinter.CTkLabel(self, text="")
        self.video_stream.grid(row=0, column=0, padx=10, pady=10, rowspan=tot_rows)

        # Frame for all buttons
        right_frame = customtkinter.CTkFrame(self, width=600, height=600)
        right_frame.grid(row=0, column=1, padx=10, pady=10, columnspan=3, rowspan=tot_rows)

        # Setup buttons
        customtkinter.CTkLabel(right_frame, text="Setup:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.zoompercent = DoubleVar()
        cam_zoom_btn = customtkinter.CTkButton(right_frame, text="Set Zoom")
        cam_zoom_btn.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        cam_zoom_slider = customtkinter.CTkSlider(right_frame, variable=self.zoompercent, from_=0, to=99, number_of_steps=99, orientation=HORIZONTAL, command=self.disp_zoompercent)
        cam_zoom_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.zoompercent.set(0)
        self.zoom_label = customtkinter.CTkLabel(right_frame, text="0", width=8)
        self.zoom_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Image processing buttons
        customtkinter.CTkLabel(right_frame, text="Joint Detection:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.img1 = customtkinter.CTkButton(right_frame, text="Picture 1", fg_color="red", state=self.img1_state, command=self.process_img1)
        self.img1.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.img2 = customtkinter.CTkButton(right_frame, text="Picture 2", fg_color="blue", state=self.img2_state, command=self.process_img2)
        self.img2.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.joint_location = customtkinter.CTkButton(right_frame, text="Weld Joint", state=self.intersection_state, command=self.joint)
        self.joint_location.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        # Material/welder setup buttons
        customtkinter.CTkLabel(right_frame, text="Material Setup:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.mat_thck = DoubleVar()
        mat_btn = customtkinter.CTkButton(right_frame, text="Set Material Thickness (mm)")
        mat_btn.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        mat_slider = customtkinter.CTkSlider(right_frame, variable=self.mat_thck, from_=0, to=9, number_of_steps=90, orientation=HORIZONTAL, command=self.disp_mat_thck)
        mat_slider.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.mat_thck.set(0)
        self.mat_label = customtkinter.CTkLabel(right_frame, text="0", width=8)
        self.mat_label.grid(row=5, column=2, padx=5, pady=5, sticky="w")

        # GCode/machine control buttons
        customtkinter.CTkLabel(right_frame, text="GCODE:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        customtkinter.CTkButton(right_frame, text="Generate G-Code", command=self.gcode).grid(row=7, column=0, padx=5, pady=5, sticky="w")
        customtkinter.CTkButton(right_frame, text="Execute").grid(row=7, column=1, padx=5, pady=5, sticky="w")

        # XYZ controller buttons
        customtkinter.CTkLabel(right_frame, text="XYZ Controller:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        xy_frame = customtkinter.CTkFrame(right_frame)
        xy_frame.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        customtkinter.CTkButton(xy_frame, text="↑").grid(row=0, column=1)
        customtkinter.CTkButton(xy_frame, text="←").grid(row=1, column=0)
        customtkinter.CTkButton(xy_frame, text="→").grid(row=1, column=2)
        customtkinter.CTkButton(xy_frame, text="↓").grid(row=2, column=1)
        
        z_frame = customtkinter.CTkFrame(right_frame)
        z_frame.grid(row=8, column=2, padx=5, pady=5, sticky="w")
        customtkinter.CTkButton(z_frame, text="+Z").grid(row=0, column=0)
        customtkinter.CTkButton(z_frame, text="-Z").grid(row=1, column=0)

        # Speed inputs
        customtkinter.CTkLabel(right_frame, text="Speed:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.xy_speed = StringVar()
        self.z_speed = StringVar()
        customtkinter.CTkLabel(right_frame, text="XY Speed:").grid(row=10, column=0, padx=5, pady=5, sticky="w")
        xy_speed_entry = customtkinter.CTkEntry(right_frame, textvariable=self.xy_speed)
        xy_speed_entry.grid(row=10, column=1, padx=5, pady=5, sticky="w")
        customtkinter.CTkLabel(right_frame, text="Z Speed:").grid(row=11, column=0, padx=5, pady=5, sticky="w")
        z_speed_entry = customtkinter.CTkEntry(right_frame, textvariable=self.z_speed)
        z_speed_entry.grid(row=11, column=1, padx=5, pady=5, sticky="w")

        # Additional buttons
        customtkinter.CTkButton(right_frame, text="Zero").grid(row=12, column=0, padx=5, pady=5, sticky="w")
        customtkinter.CTkButton(right_frame, text="Go Home").grid(row=12, column=1, padx=5, pady=5, sticky="w")

        self.open_camera()

    def disp_zoompercent(self, event=None):
        value = np.round(self.zoompercent.get(), 2)
        self.zoom_label.configure(text=f"{value}")

    def disp_mat_thck(self, event=None):
        value = np.round(self.mat_thck.get(), 2)
        self.mat_label.configure(text=f"{value}")

    def open_camera(self):
        _, self.frame = self.cap.read()
        cv2_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
        cap_img = Image.fromarray(cv2_img)
        photo_img = customtkinter.CTkImage(light_image=cap_img, size=(800, 600))
        self.video_stream.photo_img = photo_img
        self.video_stream.configure(image=photo_img)
        self.video_stream.after(10, self.open_camera)

    def process_img1(self):
        path = weld_joint.process_img(None)
        path.img_in_processing = self.frame
        path.img_crop(100, 3496, 500, 3496)
        path.img_bilateral_blur()
        path.img_detect_HSV_contours()
        path.largest_contour()

        # Empty distortion matrix because the camera has negligible distortion
        mtx = np.array([[1,0,1],[0,1,1],[0,0,1]])
        dst = np.array([[1,1,1,1,1]])

        self.corners = weld_joint.find_aruco_corners(self.frame, mtx, dst)
        self.contours2 = None
        self.joint_intersection = None
        self.contours1 = path.contours

        self.img2_state = NORMAL
        self.img2.configure(state=self.img2_state)
        self.intersection_state = DISABLED
        self.joint_location.configure(state=self.intersection_state)

    def process_img2(self):
        path = weld_joint.process_img(None)
        path.img_in_processing = self.frame
        path.img_crop(100, 3496, 500, 3496)
        path.img_bilateral_blur()
        path.img_detect_HSV_contours()
        path.largest_contour()

        self.joint_intersection = None
        self.contours2 = path.contours

        self.img2_state = DISABLED
        self.img2.configure(state=self.img2_state)
        self.intersection_state = NORMAL
        self.joint_location.configure(state=self.intersection_state)

    def joint(self):
        if self.contours1 is not None and self.contours2 is not None and self.corners is not None:
            self.joint_intersection = weld_joint.radius_intersect(self.contours1, self.contours2, radius=3)
            self.intersection_state = DISABLED
            self.joint_location.configure(state=self.intersection_state)
            self.contours1 = None
            self.contours2 = None

    def gcode(self):
        if self.path_wrt_aruco is not None:
            grbl_gcode.generate_path_gcode(self.path_wrt_aruco, 0.1205, 300)

app = App()
app.mainloop()
