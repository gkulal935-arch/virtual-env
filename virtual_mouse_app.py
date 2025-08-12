import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from tkinter import ttk
import threading
import time
from PIL import Image, ImageTk
import numpy as np

class VirtualMouseApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Virtual Mouse Control - BBHC Library")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2d3748')
        
        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7, 
            min_tracking_confidence=0.7,
            max_num_hands=1
        )
        
        # Screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Control variables
        self.is_running = False
        self.show_landmarks = True
        self.smoothing_factor = 0.5
        self.click_threshold = 30
        
        # Hand position smoothing
        self.prev_x, self.prev_y = 0, 0
        
        self.setup_ui()
        self.setup_camera()
        
    def setup_ui(self):
        # Main title
        title_frame = tk.Frame(self.root, bg='#2d3748')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame, 
            text="🎮 Virtual Mouse Control System", 
            font=('Arial', 24, 'bold'), 
            fg='white', 
            bg='#2d3748'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame, 
            text="BBHC Library Management System", 
            font=('Arial', 14), 
            fg='#a0aec0', 
            bg='#2d3748'
        )
        subtitle_label.pack()
        
        # Control panel
        control_frame = tk.Frame(self.root, bg='#4a5568', relief='raised', bd=2)
        control_frame.pack(pady=20, padx=20, fill='x')
        
        # Control buttons
        btn_frame = tk.Frame(control_frame, bg='#4a5568')
        btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(
            btn_frame, 
            text="🚀 Start Virtual Mouse", 
            command=self.start_virtual_mouse,
            font=('Arial', 12, 'bold'),
            bg='#48bb78', 
            fg='white',
            relief='raised',
            bd=3,
            padx=20,
            pady=10
        )
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(
            btn_frame, 
            text="⏹️ Stop", 
            command=self.stop_virtual_mouse,
            font=('Arial', 12, 'bold'),
            bg='#f56565', 
            fg='white',
            relief='raised',
            bd=3,
            padx=20,
            pady=10,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=10)
        
        self.back_btn = tk.Button(
            btn_frame, 
            text="🏠 Back to Library", 
            command=self.go_back,
            font=('Arial', 12, 'bold'),
            bg='#ed8936', 
            fg='white',
            relief='raised',
            bd=3,
            padx=20,
            pady=10
        )
        self.back_btn.pack(side='left', padx=10)
        
        # Settings frame
        settings_frame = tk.Frame(control_frame, bg='#4a5568')
        settings_frame.pack(pady=10)
        
        # Smoothing control
        tk.Label(settings_frame, text="Smoothing:", font=('Arial', 10), fg='white', bg='#4a5568').pack(side='left', padx=10)
        self.smoothing_var = tk.DoubleVar(value=0.5)
        smoothing_scale = tk.Scale(
            settings_frame, 
            from_=0.1, 
            to=0.9, 
            orient='horizontal',
            variable=self.smoothing_var,
            bg='#4a5568',
            fg='white',
            highlightbackground='#4a5568'
        )
        smoothing_scale.pack(side='left', padx=10)
        
        # Click threshold control
        tk.Label(settings_frame, text="Click Threshold:", font=('Arial', 10), fg='white', bg='#4a5568').pack(side='left', padx=10)
        self.threshold_var = tk.IntVar(value=30)
        threshold_scale = tk.Scale(
            settings_frame, 
            from_=10, 
            to=100, 
            orient='horizontal',
            variable=self.threshold_var,
            bg='#4a5568',
            fg='white',
            highlightbackground='#4a5568'
        )
        threshold_scale.pack(side='left', padx=10)
        
        # Options
        self.show_landmarks_var = tk.BooleanVar(value=True)
        landmarks_check = tk.Checkbutton(
            settings_frame, 
            text="Show Hand Landmarks", 
            variable=self.show_landmarks_var,
            bg='#4a5568',
            fg='white',
            selectcolor='#2d3748'
        )
        landmarks_check.pack(side='left', padx=10)
        
        # Status display
        self.status_var = tk.StringVar(value="Ready to start virtual mouse control")
        status_label = tk.Label(
            control_frame, 
            textvariable=self.status_var,
            font=('Arial', 12), 
            fg='#48bb78', 
            bg='#4a5568',
            relief='sunken',
            bd=2,
            padx=10,
            pady=5
        )
        status_label.pack(pady=10, fill='x')
        
        # Camera display
        self.camera_label = tk.Label(self.root, bg='black', relief='sunken', bd=3)
        self.camera_label.pack(pady=20)
        
        # Instructions
        instructions_frame = tk.Frame(self.root, bg='#2d3748')
        instructions_frame.pack(pady=20, fill='x')
        
        instructions_text = """
        📋 Instructions:
        • Click 'Start Virtual Mouse' to begin
        • Move your hand in front of the camera to control the mouse
        • Touch your thumb and index finger to click
        • Adjust smoothing and click threshold as needed
        • Press 'Q' on your keyboard to quit
        """
        
        instructions_label = tk.Label(
            instructions_frame, 
            text=instructions_text,
            font=('Arial', 11), 
            fg='#e2e8f0', 
            bg='#2d3748',
            justify='left'
        )
        instructions_label.pack()
        
    def setup_camera(self):
        if not self.cap.isOpened():
            self.status_var.set("Error: Cannot open camera")
            return
            
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            
            # Convert to PhotoImage
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            self.camera_label.configure(image=photo)
            self.camera_label.image = photo
            
    def start_virtual_mouse(self):
        self.is_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_var.set("Virtual mouse is running... Move your hand!")
        
        # Start virtual mouse in separate thread
        self.virtual_mouse_thread = threading.Thread(target=self.run_virtual_mouse)
        self.virtual_mouse_thread.daemon = True
        self.virtual_mouse_thread.start()
        
    def stop_virtual_mouse(self):
        self.is_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_var.set("Virtual mouse stopped")
        
    def run_virtual_mouse(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, _ = frame.shape
            
            result = self.hands.process(rgb_frame)
            
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    if self.show_landmarks_var.get():
                        self.mp_drawing.draw_landmarks(
                            frame, 
                            hand_landmarks, 
                            self.mp_hands.HAND_CONNECTIONS
                        )
                    
                    # Get index finger tip position
                    index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
                    
                    # Apply smoothing
                    smooth_x = int(self.smoothing_factor * x + (1 - self.smoothing_factor) * self.prev_x)
                    smooth_y = int(self.smoothing_factor * y + (1 - self.smoothing_factor) * self.prev_y)
                    
                    # Convert to screen coordinates
                    screen_x = int(index_finger_tip.x * self.screen_width)
                    screen_y = int(index_finger_tip.y * self.screen_height)
                    
                    # Move mouse cursor
                    pyautogui.moveTo(screen_x, screen_y)
                    
                    # Check for click gesture (thumb and index finger close)
                    thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                    thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                    
                    distance = ((thumb_x - x) ** 2 + (thumb_y - y) ** 2) ** 0.5
                    
                    if distance < self.threshold_var.get():
                        pyautogui.click()
                        cv2.putText(frame, 'CLICKED!', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        self.status_var.set("Click detected! 🖱️")
                    else:
                        self.status_var.set("Hand detected - Moving mouse cursor")
                    
                    # Update previous positions
                    self.prev_x, self.prev_y = smooth_x, smooth_y
                    
                    # Draw cursor indicator
                    cv2.circle(frame, (smooth_x, smooth_y), 10, (0, 255, 0), -1)
                    cv2.circle(frame, (smooth_x, smooth_y), 15, (0, 255, 0), 2)
            
            # Update camera display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (640, 480))
            
            # Update UI in main thread
            self.root.after(0, self.update_camera_display, frame_resized)
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.03)
            
    def update_camera_display(self, frame):
        try:
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            self.camera_label.configure(image=photo)
            self.camera_label.image = photo
        except:
            pass
            
    def go_back(self):
        self.stop_virtual_mouse()
        self.root.destroy()
        # Here you can add logic to return to the main Flask app
        
    def on_closing(self):
        self.stop_virtual_mouse()
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    app = VirtualMouseApp()
    app.run()
