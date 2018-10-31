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

out = 4 #pin der die Feldmühle anschaltet
N = 600 #Anzahl Datenpunkte

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
    rep_size = len(X)//wdhs
    for i in range(wdhs):
        maxs.append(np.amax(X[i*rep_size:(i+1)*rep_size]))
        mins.append(np.amin(X[i*rep_size:(i+1)*rep_size]))
    amp = (np.mean(maxs - mins)) / 2

def deviation(X): #amplitude
    mean = float(np.sum(X))/len(X)
    #print("mean: "mean)
    variation = np.sum((X - mean)**2)/len(X)
    #print("variation: "variation)
    return np.sqrt(variation)

A = 0.0019242 #area of segment pair [m**2]
eps0 = 8.854*10**(-12) #epsilon0 / permittivity constant [F/m]
R = 1000000 #resistor value [Ohm]
#freq = f() #[Hz]
count = 0


"""
X, duration = messung(N)
print("amount datapoints: ", len(X))
print("data/values: ", X)
print("duration: ", duration)
deviation = deviation(X)
print("deviation: ", deviation)
#plt.plot(X)
#plt.show()
print("freq: ", f(X, duration))

#GPIO.output(out, False)
#GPIO.cleanup()

"""
#Daten auswerten und vergleichen ob gespeichert werden soll
e_start = 1000
e_end = 900
try:
    while True:
        GPIO.setup(out, GPIO.OUT)
        GPIO.output(out, True) #schaltet Feldmuehle an
        time.sleep(1)
        X, duration = messung(N)
        freq = f(X, duration)
        amp = amp(X, freq)
        dev = deviation(X)
        e = amp/4*A*eps0*R*freq
        if e>=e_start:
            X = []
            count += 1
            name = "Messung"
            num = str(count)
            date_time = str(time.time())
            title = name + num + date_time
            f = open(title + ".txt","a") #der Pfad muss noch bestimmt werden
            while e>=e_end:
                #Daten speichern und plotten
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
            time.sleep(10)
except KeyboardInterrupt:
    GPIO.cleanup()
    exit()
except:
    GPIO.cleanup()

