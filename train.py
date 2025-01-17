from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Facial Recognition System")
        self.root.wm_iconbitmap("face.ico")
        
        # Title Label
        title_lbl = Label(
            self.root,
            text="🚀 T R A I N   D A T A   S E T 🚀",
            font=("Georgia", 38, "bold"),
            bg="#e6f7ff",
            fg="#003366",
            relief="ridge",
            bd=3,
            padx=10,
            pady=5
        )
        title_lbl.place(x=0, y=0, width=1530, height=60)

        # Top Image
        img_top = Image.open(r"college_images/train1.png")
        img_top = img_top.resize((1530, 325), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=1530, height=325)
        
        # Train Button
        b1_1 = Button(
            self.root,
            text="📊 TRAIN DATA",
            command=self.train_classifier,
            cursor="hand2",
            font=("Roboto", 30, "bold"),
            bg="green",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            relief="raised",
            bd=3
        )
        b1_1.place(x=350, y=380, width=320, height=60)
        
        
          
        # Add a style for visibility
        style = ttk.Style()
        style.configure(
            "custom.Horizontal.TProgressbar",
            thickness=20,
            troughcolor="#e6f7ff",
            background="#003366",
            relief="flat")

        # Progress Bar
        self.progress = ttk.Progressbar(
            self.root,
            orient=HORIZONTAL,
            length=600,
            mode="determinate",
            style="custom.Horizontal.TProgressbar"
        )
        self.progress.place(x=700, y=380, width=400, height=60)
        
        
         # Percentage Label
        self.percentage_label = Label(self.root, text="0%", font=("Arial", 40, "bold"))
        self.percentage_label.place(x=1100, y=380, height=60)  # Position the label below the progress bar

      

        # Bottom Image
        img_bottom = Image.open(r"college_images/train4.jpg")
        img_bottom = img_bottom.resize((1530, 325), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        f_lbl = Label(self.root, image=self.photoimg_bottom)
        f_lbl.place(x=0, y=440, width=1530, height=325)
        
        # Back Button
        back_btn = Button(
            self.root,
            text="⬅Back",
            font=("Courier", 20, "bold"),
            fg="white",
            bg="#007BFF",
            activebackground="#0056b3",
            activeforeground="white",
            command=self.back_to_main,
            cursor="hand2",
            relief="raised",
            bd=3
        )
        back_btn.place(x=0, y=5, width=120, height=50)

    def back_to_main(self):
        # Close the current window
        self.root.destroy()

    def train_classifier(self):
        # Directory containing training data
        data_dir = "data"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.jpg')]

        if not path:
            messagebox.showerror("Error", "No training data found in 'data' folder!")
            return

        faces = []
        ids = []

        self.progress["value"] = 0  # Reset progress bar
        self.progress["maximum"] = len(path)  # Set maximum value

        for i, image in enumerate(path):
            try:
                img = Image.open(image).convert('L')  # Convert to grayscale
                imageNp = np.array(img, 'uint8')
                
                # Extract ID from filename and validate
                try:
                    id = int(os.path.split(image)[1].split('.')[1])
                except ValueError:
                    print(f"Skipping file {image}: invalid filename format.")
                    continue

                faces.append(imageNp)
                ids.append(id)

                # Increment progress
                self.progress["value"] += 1
                percentage = int((i + 1) / len(path) * 100)
                self.percentage_label.config(text=f"{percentage}%")
                self.root.update_idletasks()

            except Exception as e:
                print(f"Error processing image {image}: {e}")
                continue

        if not faces:
            messagebox.showerror("Error", "No valid images found for training!")
            return

        try:
            # Check for the presence of LBPHFaceRecognizer
            if hasattr(cv2.face, 'LBPHFaceRecognizer_create'):
                clf = cv2.face.LBPHFaceRecognizer_create()
            else:
                raise AttributeError("OpenCV installation does not include 'cv2.face'. Please check your setup.")

            # Train the recognizer
            clf.train(faces, np.array(ids))
            clf.write("classifier.xml")

            # Set progress to maximum to indicate completion
            self.progress["value"] = self.progress["maximum"]
            messagebox.showinfo("Result", "Training completed successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to train classifier: {e}")

        finally:
            # Reset progress bar after completion
            self.progress["value"] = 0

# Run the application
if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()
