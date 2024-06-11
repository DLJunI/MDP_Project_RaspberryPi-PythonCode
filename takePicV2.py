from flask import Flask, send_file
import subprocess
import time
from PIL import Image

app = Flask(__name__)

@app.route('/capture', methods=['GET'])
def capture_image():
    image_path = '/home/raspberrypi/Desktop/_MDP/cam_image.jpg'

    # Capture the image using libcamera
    try:
        # Using libcamera-still with reduced preview time to speed up the capture
        subprocess.run(["libcamera-still", "-o", image_path, "--nopreview", "-t", "100"], check=True)
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"
    
    # Resize the image
    try:
        with Image.open(image_path) as img:
            # Resize the image to 1920x1080
            resized_img = img.resize((1920, 1080))
            resized_img.save(image_path)
    except Exception as e:
        return f"An error occurred while resizing the image: {e}"

    return send_file(image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
