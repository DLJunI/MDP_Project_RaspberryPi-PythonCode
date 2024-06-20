import gpiozero

LED_CONTROL_PIN = gpiozero.LED(18)
realTimeState = False

def ledTesting(command):
    global realTimeState
    if command == "on" or command == "ON":
        LED_CONTROL_PIN.on()
        realTimeState = True
        print("LED State :: {}".format(realTimeState))

    elif command == "off" or command == "OFF":
        LED_CONTROL_PIN.off()
        realTimeState = False
        print("LED State :: {}".format(realTimeState))

    elif command == "now" or command == "NOW":
        print("Current LED State :: {}".format(realTimeState))

try:
    while True:
        userInput = input("\n<<< Plz Choose your LED State >>>\n\n")
        print(userInput)
        ledTesting(userInput)

except KeyboardInterrupt:
    print("Shut down")
finally:
    print("Cleaning up GPIO.")
