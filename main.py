import os
import datetime
import pickle
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import face_recognition
import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1280x720+350+100")
        self.main_window.title("Attendance System")

        # Load the background image
        self.background_image = Image.open("Attendance System.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create a background label and place it
        self.background_label = tk.Label(self.main_window, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Adjust webcam feed to fit better within the border frame
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=90, y=162, width=725, height=526)  # Adjusted to fit better inside the border

        # Add buttons with modified colors and positions
        self.login_button_main_window = util.get_button(self.main_window, 'Login', '#FFB6C1', self.login)
        self.login_button_main_window.place(x=900, y=180, width=200, height=50)  # Moved right and down

        self.logout_button_main_window = util.get_button(self.main_window, 'Logout', '#D32F2F', self.logout)
        self.logout_button_main_window.place(x=900, y=280, width=200, height=50)  # Moved right and down

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register New User', '#1976D2', self.register_new_user, fg='white')
        self.register_new_user_button_main_window.place(x=900, y=380, width=200, height=50)  # Moved right and down

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        # Continue updating the webcam feed
        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        # Load all registered face encodings and names
        known_encodings = []
        known_names = []

        for file in os.listdir(self.db_dir):
            if file.endswith('.pickle'):
                with open(os.path.join(self.db_dir, file), 'rb') as f:
                    known_encodings.append(pickle.load(f))
                    known_names.append(os.path.splitext(file)[0])  # Remove .pickle extension

        # Load the unknown image and extract its encodings
        unknown_img = face_recognition.load_image_file(unknown_img_path)
        unknown_encodings = face_recognition.face_encodings(unknown_img)

        if len(unknown_encodings) > 0:
            unknown_encoding = unknown_encodings[0]

            # Compare the captured face to known faces
            results = face_recognition.compare_faces(known_encodings, unknown_encoding)

            if True in results:
                match_index = results.index(True)
                name = known_names[match_index]
                util.msg_box('Welcome back!', f'Welcome, {name}.')
            else:
                util.msg_box('OOPs...', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('Error', 'No face found. Please try again.')

        os.remove(unknown_img_path)

    def logout(self):
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        known_encodings = []
        known_names = []

        for file in os.listdir(self.db_dir):
            if file.endswith('.pickle'):
                with open(os.path.join(self.db_dir, file), 'rb') as f:
                    known_encodings.append(pickle.load(f))
                    known_names.append(os.path.splitext(file)[0])

        unknown_img = face_recognition.load_image_file(unknown_img_path)
        unknown_encodings = face_recognition.face_encodings(unknown_img)

        if len(unknown_encodings) > 0:
            unknown_encoding = unknown_encodings[0]

            results = face_recognition.compare_faces(known_encodings, unknown_encoding)

            if True in results:
                match_index = results.index(True)
                name = known_names[match_index]
                util.msg_box('Bye', f'Goodbye, {name}.')
                with open(self.log_path, 'a') as f:
                    f.write(f'{name},{datetime.datetime.now()},logout\n')
            else:
                util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('Error', 'No face found. Please try again.')

        os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', '#4CAF50', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=850, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', '#F44336', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=850, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=50, y=50, width=700, height=400)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=850, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Input Username:')
        self.text_label_register_new_user.place(x=850, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        # Encode the captured face
        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

        # Save the face encodings to a pickle file
        with open(os.path.join(self.db_dir, f'{name}.pickle'), 'wb') as file:
            pickle.dump(embeddings, file)

        # Log the registration
        with open(self.log_path, 'a') as f:
            f.write(f'{name},{datetime.datetime.now()},Registered\n')

        util.msg_box('Success!', 'User was registered successfully!')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
