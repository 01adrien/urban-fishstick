# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 23:06:54 2024

@author: Henin
"""

import RPi.GPIO as GPIO
import time

trig_pin = 17  # Remplacez par broche Trig (émetteur)


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin, GPIO.OUT)

#A modifier selon les résultats du point 2 
def emettre_bit(bit):
    if bit == 0:
        GPIO.output(trig_pin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(trig_pin, GPIO.LOW)
        time.sleep(0.1)
    elif bit == 1:
        GPIO.output(trig_pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(trig_pin, GPIO.LOW)
        time.sleep(0.1)

def emettre_paquet(message):
    for bit in message:
        emettre_bit(bit)

def main():
    setup()
    try:
        # Envoie d'une série de 50 paquets
        for i in range(50):
            message = bin(i * 5)[2:].zfill(8)  # Convertit en binaire et complète avec des zéros
            emettre_paquet(message)
            time.sleep(1)  # Attendez 1 seconde entre chaque paquet
            print("Paquet n°" + i)
            
        print("Fini")

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()