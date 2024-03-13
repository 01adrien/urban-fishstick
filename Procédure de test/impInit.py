# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:45:55 2024

@author: Henin
"""

import RPi.GPIO as GPIO
import time

trig_pin = 17  # Remplacez par le numéro de la broche Trig (émetteur)
echo_pin = 27  # Remplacez par le numéro de la broche Echo (recepteur)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

def send_pulse():
    GPIO.output(trig_pin, GPIO.HIGH) #Active ultrason
    time.sleep(0.1)
    GPIO.output(trig_pin, GPIO.LOW) #Coupe ultrason

def main():
    setup()
    
    try:
        while True:
            for _ in range(3):
                send_pulse()
                time.sleep(0.1)  # Attendre un moment entre chaque impulsion
            
            time.sleep(1)  # Attendre 1 seconde entre chaque série d'impulsions

    except KeyboardInterrupt:
        GPIO.cleanup() # Eteindre avec CTRL-C

if __name__ == "__main__":
    main()
