from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from time import strftime
from datetime import datetime
import csv
import cv2
import os
import numpy as np
import pyttsx3

# Initialize pyttsx3 engine for speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice


def speak_va(transcribed_query):
    """Function to make the system speak out the transcribed query."""
    engine.say(transcribed_query)
    engine.runAndWait()


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Facial Recognition System")
        self.root.wm_iconbitmap("face.ico")

        # Load and display images
        self.load_images()

        # Title Label
        self.create_title_label()

        # Face Recognition Button
        self.create_face_recognition_button()

        # Warning Label
        self.create_warning_label()

        # Back Button
        self.create_back_button()

        # Progressbar to show accuracy
        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, length=1530, mode="determinate")
        self.progress.place(x=40, y=50, width=400, height=60)  # Place the progress bar just below the title

        # Percentage Label to display confidence
        self.percentage_label = Label(self.root, text="0%", font=("Arial", 40, "bold"), bg="#e6e6e6", fg="#333333")
        self.percentage_label.place(x=400, y=50,height=60)  # Place the percentage label near the progress bar

    def load_images(self):
        """Load and display images for the interface."""
        img1 = Image.open(r"C:\Users\HP\Desktop\facial_recognition system\college_images\recog.jpg")
        img1 = img1.resize((500, 130), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg1).place(x=0, y=0, width=500, height=130)

        img2 = Image.open(r"C:\Users\HP\Desktop\facial_recognition system\college_images\train3.jpg")
        img2 = img2.resize((500, 130), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimg2).place(x=500, y=0, width=500, height=130)

        img3 = Image.open(r"C:\Users\HP\Desktop\facial_recognition system\college_images\recog3.jpg")
        img3 = img3.resize((600, 130), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        Label(self.root, image=self.photoimg3).place(x=1000, y=0, width=600, height=130)

        img4 = Image.open(r"C:\Users\HP\Desktop\facial_recognition system\college_images\recog5.jpg")
        img4 = img4.resize((1530, 710), Image.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)
        Label(self.root, image=self.photoimg4).place(x=0, y=130, width=1530, height=710)

    def create_title_label(self):
        """Create title label for the application."""
        title_lbl = Label(
            self.root,
            text="✨ F A C E   R E C O G N I T I O N ✨",
            font=("Georgia", 42, "bold"),
            bg="#e6e6e6",
            fg="#333333",
            relief="groove",
            bd=3
        )
        title_lbl.place(x=0, y=132, width=1530, height=70)

    def create_face_recognition_button(self):
        """Create button for face recognition."""
        b1_1 = Button(
            self.root,
            text="🎭 Face Recognition",
            cursor="hand2",
            command=self.face_recog,
            font=("Courier", 15, "bold"),
            bg="green",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            relief="raised",
            bd=3
        )
        b1_1.place(x=980, y=340, width=240, height=60)

    def create_warning_label(self):
        """Create a warning label when press Enter to terminate."""
        title_lbl = Label(
            self.root,
            text="⛔ Please Press Enter to Terminate ⛔",
            font=("Georgia", 18, "bold"),
            bg="#ffcccc",
            fg="darkred",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        title_lbl.place(x=750, y=500, width=500, height=50)

    def create_back_button(self):
        """Create a back button."""
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
        back_btn.place(x=0, y=132, width=120, height=68)

    def back_to_main(self):
        """Back to the main window."""
        self.root.destroy()  # Close the current window

    def mark_attendance(self, student_id, roll_no, student_name, department):
        """Mark attendance for the recognized student."""
        if not os.path.isfile("Student_attendance_list.csv"):
            with open("Student_attendance_list.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Student ID", "Roll No", "Name", "Date", "Time", "Status"])

        # Check if student attendance is already marked
        with open("Student_attendance_list.csv", "r+", newline="\n") as f:
            my_data = f.readlines()
            name_list = [line.split(",")[0] for line in my_data]

            if str(student_id) not in name_list:
                now = datetime.now()
                current_date = now.strftime("%d/%m/%Y")
                current_time = now.strftime("%H:%M:%S")
                f.writelines(f"\n{student_id},{roll_no},{student_name},{department},{current_time},{current_date},Present")

    def face_recog(self):
        """Main function to handle face recognition."""
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            """Detect faces and display the bounding box and student info."""
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            coord = []

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                # Update the progress bar and percentage label
                self.progress['value'] = confidence
                self.percentage_label.config(text=f"{confidence}%")  # Update the percentage label
                self.root.update_idletasks()  # Update the Tkinter GUI

                # MySQL connection
                try:
                    conn = mysql.connector.connect(host="localhost", username="root", password="admin@2309", database="fras")
                    my_cursor = conn.cursor()
                    my_cursor.execute(f"SELECT Student_id, Roll_No, Student_Name, Department FROM student WHERE Student_id = {id}")
                    student_data = my_cursor.fetchone()
                    if student_data:
                        student_id, roll_no, student_name, department = student_data
                    else:
                        student_id = roll_no = student_name = department = "Unknown"
                except mysql.connector.Error as err:
                    student_id = roll_no = student_name = department = "Error"
                    print(f"Error: {err}")
                finally:
                    conn.close()

                if confidence > 77:
                    cv2.putText(img, f"Student_id:{student_id}", (x, y - 95), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll:{roll_no}", (x, y - 65), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name:{student_name}", (x, y - 35), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Department:{department}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.mark_attendance(student_id, roll_no, student_name, department)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                coord = [x, y, w, h]
            return coord

        def recognize(img, clf, face_cascade):
            """Recognize the faces from the webcam feed."""
            coord = draw_boundary(img, face_cascade, 1.1, 10, (255, 255, 255), "Face", clf)
            return img

        # Load pre-trained classifier and face cascade
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        # Initialize webcam capture
        video_cap = cv2.VideoCapture(0)

        if not video_cap.isOpened():
            print("Error: Could not open webcam.")
            return

        while True:
            ret, img = video_cap.read()
            if not ret or img is None:  # Check if frame is successfully captured
                print("Error: Failed to capture image")
                break
            img = recognize(img, clf, face_cascade)
            cv2.imshow("Welcome To Face Recognition", img)

            if cv2.waitKey(1) == 13:  # Enter key to stop
                break

        # Release the webcam and close OpenCV windows
        video_cap.release()
        cv2.destroyAllWindows()

# Create the GUI window
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()