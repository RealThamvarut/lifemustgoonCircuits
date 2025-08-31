from service.upload_google import ESPCAMDriveUploader

#need client_secret.json
def main():
    ESPCAM_IP = "192.168.1.105"

    uploader = ESPCAMDriveUploader( #need client_secrets.json to be in the same folder as python file we run
        ESPCAM_ip=ESPCAM_IP,
        folder_id="1dcXa6NMK8xF6Cq1ojAuWLIGZRhY_Ca2-" 
    )

    try:
        print("Capturing image")
        img_bytes = uploader.capture_image_bytes() # this will capture the image from the ESP32 camera
        print(f"Captured: {len(img_bytes)} bytes")

        filename = uploader.generate_filename() #generate file name for the image
        print(f"Uploading image as {filename}")
        uploader.upload_image_bytes(img_bytes, filename) #upload the image
        print(f"Upload complete")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()