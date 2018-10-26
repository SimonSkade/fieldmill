#import os
#import sys
import RPi.GPIO as GPIO
import time
#import matplotlib.pyplot as plt
import Adafruit_ADS1x15
#import keyboard
import numpy as np

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()


# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 Xsheet for more info on gain.
GAIN = 2/3

GPIO.setmode(GPIO.BCM)

out = 4

N = 40
GPIO.setup(out, GPIO.OUT)

def messung(N):
    X = []
    a = time.time()
    for i in range(N):
        X.append(adc.read_adc_difference(0, gain=GAIN))
    duration = time.time() - a
    return np.asarray(X), duration


GPIO.output(out, True) #schaltet Feldmuehle an

time.sleep(3)

def f(X, duration): #frequency
    fft = np.fft.fft(X) #/len(X)
    print(fft)
    max=0
    plt.plot(frq,abs(Y),'r') # plotting the spectrum
    plt.set_xlabel('Freq (Hz)')
    plt.set_ylabel('|Y(freq)|')
    plt.show()

    for i in range(len(fft)):
        if fft[i]>max:
            max=fft[i]
            index = i
    freq = index*duration/len(fft)
    return freq


def deviation(X): #amplitude
    mean = float(np.sum(X))/len(X)
    print(mean)
    variation = np.sum((X - mean)**2)/len(X)
    print(variation)
    return np.sqrt(variation)

A = 22 #area
eps0 = 0.00000000000885 #epsilon0 / permittivity constant
R = 1000000 #resistor value
#freq = f()
count = 0


X, duration = messung(N)
print("X: ", X)
print("duration: ", duration)
deviation = deviation(X)
print("deviation: ", deviation)
#plt.plot(X)
#plt.show()
#print("freq: ", f(X, duration))
GPIO.cleanup()

"""
#Daten auswerten und vergleichen ob gespeichert werden soll
e_start = 1000
e_end = 900
try:
    while True:
        e = amp()/4*A*eps0*R*freq
        if e>=e_start:
            X = []
            count += 1
            #time.start()
            #e_max = e
            name = "Messung"
            num = str(count)
            date_time = str(time.time())
            title = name + num + date_time
            f = open(title + ".txt","a") #der Pfad muss noch bestimmt werden
            while e>=e_end:
                #Daten speichern und plotten
                #if e>=e_max:
                #    e_max=e
                e = amp()/4*A*eps0*R*freq
                e_str = str(e)
                f.write(e_str)
                X.append([time.time(), e])
                time.sleep(0.01)
            #time.end()
            plt.figure(0)
            plt.plot(X[:,0], X[:,1])
            plt.savefig(title + ".png") #der Pfad muss noch bestimmt werden
        else:
            time.sleep(0.2)
        if keyboard.is_pressed('q'):
            break
except KeyboardInterrupt:
    GPIO.cleanup()
    exit()



GPIO.cleanup()

"""
