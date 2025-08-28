from service.upload_google import ESPCAMDriveUploader

#need client_secret.json
def main():
    ESPCAM_IP = "192.168.1.105"

    uploader = ESPCAMDriveUploader(
        ESPCAM_ip=ESPCAM_IP,
        folder_id="1dcXa6NMK8xF6Cq1ojAuWLIGZRhY_Ca2-"
    )

    try:
        print("Capturing image")
        img_bytes = uploader.capture_image_bytes()
        print(f"Captured: {len(img_bytes)} bytes")

        filename = "test_esp32_capture.jpg"
        print(f"Uploading image as {filename}")
        uploader.upload_image_bytes(img_bytes, filename)
        print(f"Upload complete")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()