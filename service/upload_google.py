import requests
import io
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth


#insert ip as x.x.x.x
class ESPCAMDriveUploader:
    def __init__(self, ESPCAM_ip: str, folder_id: str, credentials="credentials.json"):
        self.credentials = credentials
        self.drive = self.authenticate_google_drive()
        self.folder_id = folder_id
        if self.try_camera(ESPCAM_ip) is not None:
            self.ESPCAM_ip = self.try_camera(ESPCAM_ip)
        else:
            self.ESPCAM_ip = self.try_camera_iterate_on_error(ESPCAM_ip)

    #google drive authenticate
    def authenticate_google_drive(self):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(self.credentials)
        
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile(self.credentials)
        return GoogleDrive(gauth)

    def try_camera(self, ESPCAM_ip:str):
        ip = f"http://{ESPCAM_ip}/capture"
        try:
            response = requests.get(ip, timeout=2)
            if response.status_code == 200:
                print(f"Camera found at: {ESPCAM_ip}")
                return ESPCAM_ip
        except Exception as e:
            print(f"Error occurred: {e}")
        return None

    def try_camera_iterate_on_error(self, ESPCAM_ip: str):
        RANGE = 255
        for i in range(RANGE):
            #split
            ip_parts = ESPCAM_ip.split('.')
            ip_parts[-1] = str(i)
            new_ip = '.'.join(ip_parts)
            print(f"Trying camera at: {new_ip}")

            ip = f"http://{new_ip}/capture"
            try:
                response = requests.get(ip, timeout=2)
                if response.status_code == 200:
                    print(f"Camera found at: {new_ip}")
                    return new_ip
            except Exception as e:
                print(f"Error occurred: {e}")
        return None

    def capture_image_bytes(self) -> bytes:
        response = requests.get(f"http://{self.ESPCAM_ip}/capture", timeout=5)
        if response.status_code == 200:
            return response.content
        else: 
            raise Exception(f"Failed to capture image from ESPCAM-CAM. Status code: {response.status_code}")

    def upload_image_bytes(self, image_bytes: bytes):
        with io.BytesIO(image_bytes) as f:
            with open("temp.jpg", "wb") as tmp:
                tmp.write(f.read())
            
            file = self.drive.CreateFile(
                {'title': self.generate_filename(),
                 'parents': [{'id': self.folder_id}]
                 })
            file.SetContentFile("temp.jpg")
            file.Upload()
            return file['id']

    def generate_filename(self):
        from datetime import datetime
        now = datetime.now()
        return now.strftime("esp32_image_%Y%m%d_%H%M%S.jpg")