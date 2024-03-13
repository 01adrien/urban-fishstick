"""
Created on Wed Mar 13 10:51:33 2024

@author: Henin
"""

import RPi.GPIO as GPIO
import time

echo_pin = 24  # Remplacez par broche Echo (récepteur)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(echo_pin, GPIO.IN)

def get_pulse_duration():
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    return pulse_duration

def main():
    setup()

    try:
        while True:
            pulse_duration = get_pulse_duration()
            print("Durée de l'impulsion : {:.2f} secondes".format(pulse_duration))

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()