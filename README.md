# Face-Attendance-System
Introduction
- This is a face recognition-based attendance system built using Python, OpenCV, and face_recognition libraries. The system allows users to register new users, login, and logout, and keeps a record of attendance.

Features
- Register new users with face recognition
- Login and logout functionality
- Attendance record keeping
- Real-time webcam feed display

Prerequisites:
To run this application, you need to have the following installed:
- Python 3.7 or later
- OpenCV (pip install opencv-python)
- face_recognition (pip install face_recognition)
- Pillow (pip install pillow)
- Tkinter (pip install tk)
  
Usage
- Run the application and a window will appear with a webcam feed.
- Click on the "Register New User" button to register a new user.
- Enter the username and click on the "Accept" button to save the face encodings.
- Click on the "Login" button to login using face recognition.
- Click on the "Logout" button to logout and record the attendance.
  
Technical Details
- The application uses the face_recognition library to recognize faces and compare them with the registered faces.
- The OpenCV library is used to capture and display the webcam feed.
- The Tkinter library is used to create the GUI.
- The attendance record is kept in a text file (log.txt)
  
Acknowledgments
- The face_recognition library is used for face recognition.
- The OpenCV library is used for webcam feed capture and display.
- The Tkinter library is used for GUI creation.
