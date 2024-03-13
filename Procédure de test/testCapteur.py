# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:39:55 2024

@author: Henin
"""

import RPi.GPIO as GPIO
import time

trig_pin = 17  # Remplacez par le numéro de la broche Trig
echo_pin = 27  # Remplacez par le numéro de la broche Echo

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin, GPIO.OUT) # Définit trig_pin étant la sortie (émetteur)
    GPIO.setup(echo_pin, GPIO.IN) # Définit echo_pin étant la sortie (récepteur)

def get_distance():
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)

    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # converti la durée en distance (distance en cm)
    distance = round(distance, 2)

    return distance

def main():
    setup()
    
    try:
        while True:
            distance = get_distance()
            print("Distance : {} cm".format(distance))
            time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()