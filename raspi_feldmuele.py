#import os
#import sys
import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import Adafruit_ADS1x15
#import keyboard
import numpy as np
import datetime

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

out = 4 #pin der die Feldmühle anschaltet
N = 200 #Anzahl Datenpunkte

def messung(N):
    X = []
    a = time.time()
    for i in range(N):
        X.append(adc.read_adc_difference(0, gain=GAIN))
    duration = time.time() - a
    return np.asarray(X), duration


def f(X, duration): #frequency
    fft = np.fft.fft(X) #/len(X)
    n = len(fft)//2 + 1
    Y = np.abs(fft[:n])

    st = duration/len(X)
    sf = 1/st
    x_ax = np.linspace(0, sf/2, n)
    
    #print(Y)
    #plt.plot(x_ax,abs(Y),'r') # plotting the spectrum
    #plt.set_xlabel('Freq (Hz)')
    #plt.show()
    val_max = 0
    for i, val in enumerate(Y): #search index of the highest value in fft
        if val > val_max:
            val_max = val
            index = i
    freq = x_ax[index]
    return freq

def amp(X, freq, duration):
    maxs = []
    mins = []
    wdhs = duration*freq
    wdhs = int(wdhs)
    rep_size = len(X)//wdhs
    for i in range(wdhs):
        maxs.append(np.amax(X[i*rep_size:(i+1)*rep_size]))
        mins.append(np.amin(X[i*rep_size:(i+1)*rep_size]))
    amp = (np.mean(np.asarray(maxs) - np.asarray(mins))) / 2
    return amp

def deviation(X): #amplitude
    mean = float(np.sum(X))/len(X)
    #print("mean: "mean)
    variation = np.sum((X - mean)**2)/len(X)
    #print("variation: "variation)
    return np.sqrt(variation)

A = 0.0019242 #area of segment pair [m**2]
EPS0 = 8.854*10**(-12) #epsilon0 / permittivity constant [F/m]
R = 1000000 #resistor value [Ohm]
#freq = f() #[Hz]
count = 0

max_val = 2**16
wide = 2*6.144 # bitte bei GAIN einstellungen nachschauen.
"""
X, duration = messung(N)
print("amount datapoints: ", len(X))
print("data/values: ", X)
print("duration: ", duration)
deviation = deviation(X)
print("deviation: ", deviation)
#plt.plot(X)
#plt.show()
freq=f(X, duration
print("freq: ", freq))
amp=amp(X, freq
print("amp: ", amp))
print("E = ", amp/4*A*eps0*R*freq)
#GPIO.output(out, False)
#GPIO.cleanup()
"""
#Daten auswerten und vergleichen ob gespeichert werden soll
e_start = 3000
e_end = 2800
try:
    while True:
        GPIO.setup(out, GPIO.OUT)
        GPIO.output(out, True) #schaltet Feldmuehle an
        time.sleep(1)
        X, duration = messung(N)
        freq = f(X, duration)
        amplitude = amp(X, freq, duration)
        dev = deviation(X)
        e = amplitude/(4*A*EPS0*R*freq) * wide / max_val
        print("E = {}, amp = {}, freq = {}, deviation = {}, duration = {}".format(e, amplitude, freq, dev, duration))
        if e>=e_start:
            Y = []
            count += 1
            name = "Messung_"
            num = str(count)
            date_time = str(datetime.datetime.now())
            title = name + num + '_' + date_time
            file = open("results/" + title + ".txt","a")
            while e>=e_end: #Daten speichern und plotten
                GPIO.setup(out, GPIO.OUT)
                GPIO.output(out, True) #schaltet Feldmuehle an
                time.sleep(1)
                X, duration = messung(N)
                freq = f(X, duration)
                amplitude = amp(X, freq, duration)
                dev = deviation(X)
                e = amplitude/(4*A*EPS0*R*freq) * wide / max_val
                print("E = {}, amp = {}, freq = {}, deviation = {}, duration = {}".format(e, amplitude, freq, dev, duration))
                
                e_str = str(e)
                file.write(str(time.time()) + ' ' + e_str + '\n')
                Y.append([time.time(), e])
                time.sleep(0.1)
            #Y = np.array(Y)
            #plt.plot(Y[:,0], Y[:,1])
            #plt.savefig("results/" + title + ".png")
            file.close()
        else:
            time.sleep(10)
except KeyboardInterrupt:
    GPIO.cleanup()

