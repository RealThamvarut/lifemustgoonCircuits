# camera.py
from picamera2 import Picamera2
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import cv2
import time

class PI5CAMDriveUploader:
    def __init__(self):
        # Initialize camera
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration())
        self.picam2.start()

        # Google Drive init
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

    def capture_and_upload(self):
        filename = f"capture_{int(time.time())}.jpg"

        # Capture frame
        frame = self.picam2.capture_array()
        cv2.imwrite(filename, frame)

        # Upload
        file_drive = self.drive.CreateFile({'title': filename})
        file_drive.SetContentFile(filename)
        file_drive.Upload()

        return filename
