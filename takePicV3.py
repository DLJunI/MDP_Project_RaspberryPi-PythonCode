
# ---------- import zone [Start] ----------
from flask import Flask, send_file
import subprocess
import os
from PIL import Image
import RPi.GPIO as GPIO
# ---------- import zone [End] ----------



# ---------- GPIO Setup [Start] ----------
LED_CONTROL_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_CONTROL_PIN, GPIO.OUT)
# ---------- GPIO Setup [End] ----------



# ---------- Flask Route and function define zone [Start] ----------
app = Flask(__name__)

@app.route('/capture', methods=['GET'])
def capture_image():
    image_path = '/home/raspberrypi/Desktop/_MDP/cam_image.jpg'
    temp_image_path = '/home/raspberrypi/Desktop/_MDP/temp_cam_image.jpg'

    # Capture the image using libcamera
    try:
        # Using libcamera-still with reduced preview time to speed up the capture
        subprocess.run(["libcamera-still", "-o", temp_image_path, "--nopreview", "-t", "100"], check=True)
    except subprocess.CalledProcessError as e:
        return f"An error occurred while capturing the image: {e}"

    # Check if the image was captured
    if not os.path.exists(temp_image_path):
        return "Image capture failed, file does not exist."

    # Resize the image
    try:
        with Image.open(temp_image_path) as img:
            # Resize the image to 1920x1080
            resized_img = img.resize((1920, 1080))
            resized_img.save(image_path)
    except Exception as e:
        return f"An error occurred while resizing the image: {e}"

    # Check if the image was resized and saved
    if not os.path.exists(image_path):
        return "Image resizing failed, file does not exist."

    return send_file(image_path, mimetype='image/jpeg')


@app.route('/led/on', methods=['GET'])
def led_on():
    try:
        GPIO.output(LED_CONTROL_PIN, GPIO.HIGH)
        return "LED is ON"
    except Exception as e:
        return f"An error occurred while turning on the LED: {e}"


@app.route('/led/off', methods=['GET'])
def led_off():
    try:
        GPIO.output(LED_CONTROL_PIN, GPIO.LOW)
        return "LED is OFF"
    except Exception as e:
        return f"An error occurred while turning off the LED: {e}"
    
    
# ---------- Flask Route and function define zone [End] ----------



# ---------- main [Start]----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# ---------- main [End]----------