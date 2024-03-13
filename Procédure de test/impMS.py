# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 22:53:37 2024

@author: Henin
"""
import RPi.GPIO as GPIO
import time

trig_pin = 17  # Remplacez par broche Trig (émetteur)
# Séquence d'impulsions
impulsions = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500]


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin, GPIO.OUT)

# Fonction pour émettre une impulsion
def emettre_impulsion(duree):
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(duree / 1000.0)  # Convertit la durée en secondes
    GPIO.output(trig_pin, GPIO.LOW)


def main():
    setup()
    
    try:
        for impulsion in impulsions:
            emettre_impulsion(impulsion)
            time.sleep(1) 

    except KeyboardInterrupt:
        GPIO.cleanup() # Eteindre avec CTRL-C

if __name__ == "__main__":
    main()
