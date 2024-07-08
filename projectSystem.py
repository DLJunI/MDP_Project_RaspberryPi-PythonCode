# latest version[1.0] combines with LED Control and Take Picture

# Code Execution Conditions {
#   1. activate Virtual Environment [ source /home/raspberrypi/myenv/bin/activate ]
#   2. enable Port:5000 [ sudo ufw enable (if you have allowed before,[ sudo ufw allow 5000 ]) ]
#   3. disable ufw [ sudo ufw disable (if you don't close ufw, you can't access with VNC) ] 
#}

# patch note {
#    2024.06.04 Create an integrated project [Ver 1.0]
#    2024.06.18 Change " LED_PIN " variable name -> "LED_CONTROL_PIN" [Ver 1.0.1]
#    2024.06.20 Modified to LED control code using gpiozero due to RPi.GPIO unavailability [Ver 1.1.1]
#    2024.06.27 add servomotor control code for open/close [Ver 1.2.0]
#
#}

# ---------- import zone [Start] ----------
from flask import Flask, send_file
import subprocess
import os
from PIL import Image
import gpiozero
# ---------- import zone [End] ----------

# ---------- import zone [Start] ----------
from flask import Flask, send_file
import subprocess
import os
from PIL import Image
import gpiozero
# ---------- import zone [End] ----------

# ---------- GPIO Setup [Start] ----------
LED_CONTROL_PIN = gpiozero.LED(18)
SERVO_MOTOR_PIN = 2

servo1 = gpiozero.Servo(SERVO_MOTOR_PIN, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
# ---------- GPIO Setup [End] ----------

# ---------- Operation define zone [Start] ----------
def setServoAngle(servo, current_angle, target_angle):
    if abs(target_angle - current_angle) < 50:
        return current_angle
    
    servo.value = (target_angle / 90) - 1
    return target_angle
# ---------- Operation define zone [End] ----------

# ---------- Flask Route and function define zone [Start] ----------
app = Flask(__name__)

current_angle = 90

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
        LED_CONTROL_PIN.on()
        return "LED is ON"
    except Exception as e:
        return f"An error occurred while turning on the LED: {e}"

@app.route('/led/off', methods=['GET'])
def led_off():
    try:
        LED_CONTROL_PIN.off()
        return "LED is OFF"
    except Exception as e:
        return f"An error occurred while turning off the LED: {e}"

@app.route('/door/open', methods=['GET'])
def door_open():
    global current_angle
    try:
        current_angle = setServoAngle(servo1, current_angle, 10)
        return "Door is opened"
    except Exception as e:
        return f"An error occurred while opening the door: {e}"

@app.route('/door/close', methods=['GET'])
def door_close():
    global current_angle
    try:
        current_angle = setServoAngle(servo1, current_angle, 90)
        return "Door is closed"
    except Exception as e:
        return f"An error occurred while closing the door: {e}"
# ---------- Flask Route and function define zone [End] ----------

# Here's main
if __name__ == '__main__':
    current_angle = setServoAngle(servo1, 90, 90)
    app.run(host='0.0.0.0', port=5000)
    
