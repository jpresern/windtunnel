#!/usr/bin/env python3

"""
This program controls ESC for model electromotors via RPi and Adafruit HAT.
The flask part is adapated from http://mattrichardson.com/Raspberry-Pi-Flask/

"""
from flask import Flask, render_template, request
from wind_controller import WindController

app = Flask(__name__)
wc = WindController(n_motors=1)

# Create a dictionary called pins to store the pin number, name, and pin state:
buttons = {
    1: {'name': 'arm', 'state': 'disarmed'},
    2: {'name': 'start', 'state': 'disabled', 'speed': 'none'},
    3: {'name': 'stop', 'state': 'disabled'},
    4: {'name': 'accelerate', 'state': 'disabled'},
    5: {'name': 'decelerate', 'state': 'disabled'}
   }

pFreq = int(wc.pwmFreq)
pStop = int(wc.pwmDict[pFreq][0])
pStart = int(wc.pwmDict[pFreq][1])
pMax = int(wc.pwmDict[pFreq][2])

# for pin in pins:
#    GPIO.setup(pin, GPIO.OUT)
#    GPIO.output(pin, GPIO.LOW)

@app.route('/')
def index():
    # return render_template('main.html')
    # return 'Hello world'
    templateData = {
        'buttons': buttons
    }
    # Pass the template data into the template main.html and return it to the user
    return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<button_no>/<action>")
def action(button_no, action):

    # Convert the pin from the URL into an integer:
    button_no = int(button_no)

    # Get the device name for the pin being changed:
    buttonName = buttons[button_no]['name']

    # If the action part of the URL is "on," execute the code indented below:
    if action == "arm":

        print('arm motor')
        # Save the status message to be passed into the template:
        message = "Armed "
        wc.armMotors()
        speed = wc.getPWM(0)
        buttons[1]['state'] = 'armed'
        buttons[2]['state'] = 'stopped'
        buttons[3]['state'] = 'stopped'
        buttons[3]['speed'] = 'none'
        buttons[4]['state'] = 'stopped'
        buttons[5]['state'] = 'stopped'

    if action == "stop":
        print('stopped')
        message = "Turned motor off."
        wc.stopMotors()
        speed = wc.getPWM(0)
        buttons[1]['state'] = 'armed'
        buttons[2]['state'] = 'stopped'
        buttons[3]['state'] = 'stopped'
        buttons[3]['speed'] = pStop
        buttons[4]['state'] = 'stopped'
        buttons[5]['state'] = 'stopped'

    if action == "start":
        print('started')
        # speed = wc.getPWM(0)
        speed = pStart
        wc.setPwmForAllMotors(speed)
        message = "Speed set to: " + str(speed)
        buttons[1]['state'] = 'armed'
        buttons[2]['state'] = 'running'
        buttons[3]['state'] = 'running'
        buttons[3]['speed'] = 'pStart'
        buttons[4]['state'] = 'running'
        buttons[5]['state'] = 'running'

    if action == "accelerate":
        print('increase throttle')
        # buttons[4]['state'] = 'running'
        speed = wc.getPWM(0)
        if speed >= pMax:
            speed += 0
            message = "faster can't go"
            buttons[1]['state'] = 'armed'
            buttons[2]['state'] = 'running'
            buttons[3]['state'] = 'running'
            buttons[3]['speed'] = speed
            buttons[4]['state'] = 'running'
            buttons[5]['state'] = 'running'
        else:
            speed += 1
            wc.setPwmForAllMotors(speed)
            message = "speed set to: " + str(speed)
            buttons[1]['state'] = 'armed'
            buttons[2]['state'] = 'running'
            buttons[3]['state'] = 'running'
            buttons[3]['speed'] = speed
            buttons[4]['state'] = 'running'
            buttons[5]['state'] = 'running'

    if action == "decelerate":
        print('decrease throttle')
        # buttons[5]['state'] = 'running'
        speed = wc.getPWM(0)
        if speed > pStart:
            speed -= 1
            wc.setPwmForAllMotors(speed)
            message = "speed set to: " + str(speed)
            buttons[1]['state'] = 'armed'
            buttons[2]['state'] = 'running'
            buttons[3]['state'] = 'running'
            buttons[3]['speed'] = speed
            buttons[4]['state'] = 'running'
            buttons[5]['state'] = 'running'
        elif speed <= pStart:
            wc.stopMotors()
            speed = wc.getPWM(0)
            buttons[1]['state'] = 'armed'
            buttons[2]['state'] = 'stopped'
            buttons[3]['state'] = 'stopped'
            buttons[3]['speed'] = speed
            buttons[4]['state'] = 'stopped'
            buttons[5]['state'] = 'stopped'
            message = "Turned motor off."

    templateData = {
        'message': message,
        'buttons': buttons
        }

    return render_template('main.html', **templateData), speed


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
