from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import imageio
from threading import Thread
import os
import numpy as np
import tensorflow as tf

# Load your pre-trained model (replace the file path with your model)
model = tf.keras.models.load_model('kidney_stone_model.h5')

# Function to preprocess the image before prediction
def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((150, 150))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Function to predict kidney stone from the uploaded image
def predict_kidney_stone(image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    return "No Kidney Stone Detected" if prediction[0] > 0.5 else "Kidney Stone Detected"

# Function to handle image upload and prediction
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((500, 500))
        img = ImageTk.PhotoImage(img)

        panel.config(image=img)
        panel.image = img  # Keep reference of the image to prevent garbage collection
        
        # Perform prediction
        result = predict_kidney_stone(file_path)
        result_label.config(text=result)

# Function to play video in the background and resize to fit the window
def play_video(video_path, label):
    while True:  # Infinite loop to play video continuously
        vid = imageio.get_reader(video_path)
        try:
            for frame in vid:
                # Resize the frame to fit the window
                img_frame = Image.fromarray(frame)
                
                # Get current window size
                window_width = label.winfo_width()
                window_height = label.winfo_height()

                # Resize the image to fit the window
                img_frame = img_frame.resize((window_width, window_height), Image.ANTIALIAS)
                img_frame = ImageTk.PhotoImage(img_frame)
                
                label.config(image=img_frame)
                label.image = img_frame
                label.update()
        except Exception as e:
            print(f"Error playing video: {e}")

# Function to switch from the initial screen to the detection screen
def open_detection():
    # Clear the existing widgets in the window
    for widget in root.winfo_children():
        widget.destroy()

    # Header frame
    header_frame = Frame(root, bg="#4a90e2")
    header_frame.pack(fill=X)

    heading_label = Label(header_frame, text="Kidney Stone Detection System", bg="#f0e6f6", fg="#4a90e2", font=("Helvetica", 16))
    heading_label.pack(pady=20)

    # Main frame
    main_frame = Frame(root, bg="#f0e6f6")
    main_frame.pack(fill=BOTH, expand=True)

    # Image frame
    image_frame = Frame(main_frame, bg="#f0e6f6")
    image_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Label to display the uploaded image
    global panel
    panel = Label(image_frame, bg="#f0e6f6")
    panel.pack(fill=BOTH, expand=True)

    # Button frame
    button_frame = Frame(main_frame, bg="#f0e6f6")
    button_frame.pack(side=RIGHT, fill=Y)

    # Button to upload an image
    upload_button = Button(button_frame, text="Upload Image", command=upload_image, bg="#4a90e2", fg="white", font=("Helvetica", 14), bd=0, relief="flat")
    upload_button.pack(pady=10)

    # Result frame
    result_frame = Frame(main_frame, bg="#f0e6f6")
    result_frame.pack(side=LEFT, fill=X)

    # Label to display the result of the prediction
    global result_label
    result_label = Label(result_frame, text="", bg="#f0e6f6", fg="#4a90e2", font=("Helvetica", 16))
    result_label.pack(pady=10)

# Tkinter GUI setup
root = Tk()
root.title("Kidney Stone Detection System")
root.geometry("1000x1000")
root.config(bg="#f0e6f6")

# Frame for the background video
video_frame = Label(root)
video_frame.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=1, relheight=1)

# Play video in a separate thread
video_path = 'C:/Users/User/Desktop/projects/mini_project/Kidney_stone_detection_final(1st)/KS.mp4'  # Replace with the path to your video file
video_thread = Thread(target=play_video, args=(video_path, video_frame))
video_thread.daemon = True
video_thread.start()

# Frame for the text content with semi-transparent background
content_frame = Frame(root, bg="#4a90e2", bd=5, relief=RAISED)
content_frame.place(relx=0.5, rely=0.75, anchor=CENTER)

# Heading Label
heading_label = Label(content_frame, text="Kidney Stone Detection", bg="#4a90e2", fg="#f0e6f6", 
                      font=("Helvetica", 24, "bold"))
heading_label.pack(pady=10)

# Text information
info_text = "Welcome to the Kidney Stone Detection System. Upload your image to check for kidney stones using our AI-powered detection."
info_label = Label(content_frame, text=info_text, bg="#4a90e2", fg="#f0e6f6", 
                   font=("Helvetica", 14), wraplength=500, justify=CENTER)
info_label.pack(pady=20)

# Add a modern button to open the detection screen
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), padding=10)
upload_button = ttk.Button(content_frame, text="Kidney Detection", command=open_detection, style="TButton")
upload_button.pack(pady=20)

# Start the GUI loop
root.mainloop()
