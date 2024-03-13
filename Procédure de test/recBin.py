# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 23:23:35 2024

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

#Selon point 2
def recevoir_bit():
    pulse_duration = get_pulse_duration()

    if 0.09 < pulse_duration < 0.11:
        return 0
    elif 0.49 < pulse_duration < 0.51:
        return 1
    else:
        return -1  # Retourne -1 pour indiquer une erreur de réception

def recevoir_paquet():
    paquet = []
    for _ in range(8):
        bit = recevoir_bit()
        paquet.append(bit)
    return paquet

def analyser_taux_erreur(paquets_recus):
    erreurs = 0
    num_paquet = 1
    for paquet in paquets_recus:
        if paquet != num_paquet * 5:
            erreurs += 1
        num_paquet +=1
    taux_erreur = 100 - ( 2 * erreurs)
    return taux_erreur

def main():
    i = 0
    setup()
    paquets_recus = []
    try:
        while True:
            paquet = recevoir_paquet()
            message = int("".join(map(str, paquet)), 2)
            paquets_recus.append(message)
            print("Paquet reçu : {}".format(message))
            print("Num de paquet reçu   :" + i)

    except KeyboardInterrupt:
        GPIO.cleanup()
        analyser_taux_erreur(paquets_recus)

if __name__ == "__main__":
    main()