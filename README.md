#  The Fieldmill

##  What is a fieldmill?

A fieldmill is a measuring device for determining the electric field strength.

###  Construction

The field mill consists of a copper plate, which has four major segments. These segments are uniform sections of a circle, each of which is connected to the opposite segment.
Approximately Half a centimeter above the copper plate is a rotor, which is also made of copper, attached. This is shaped like two opposing segments. The rotor can rotate by an electric motor.
The electric motor is connected to a power source and can be switched on by a switch / transistor.
On two adjacent segments, a 1M ohm resistor is connected between the front and back of the board.

###  How it works

The copper segments gain charge from the electric field in the air. When the rotor comes over a segment, it absorbes the charges so that the segment gets less and vice versa when the rotor moves away from a segment.
Through that, there is a potential difference which results in voltage and current.
Over the 1M ohm resistor, we measure the voltage. We can calculate the sensitivity (you see how in Instructions-->Program-->find limit) to find out the actual electric field out of our voltage output.

In our case the output voltage goes to a analog digital converter (we use the ADS1115) and then to the raspberry pi (zero W). If a high limit is touched, the pi saves the data, so we can analyze the data.

###  What is it good for?

Inside of a thunderstorm, the electric field is very much higher than normally. So field mills are used to determine the risk of being striked by a lightning for example as a rocket launch criteria.
Further it is used to determine the electric field in laboratories for checking the experiment conditions.
Also it is just an interesting measuring device.

##  Instruction

###  Hardware

You need a filedmill. You may need to design and build one on your own. Maybe you find an instruction on the internet.
I am trying to release the cnc models we used for our fieldmill (I have not desingned them myself).

You need a raspberry pi. (We are using a raspberry pi zero W, but every Pi works. A wireless connection opportunity is recommended. Further you need an ADC. We recommend the ADS1115, because then you can just run our program.

####  Wirering



###  Software

First clone this git repository to your raspberry pi. You may do this in linux by typing
`git clone _link_`
into the terminal. (If it does not work type `sudo apt-get install git` and try it again)
Cd into the cloned directory: `cd Fieldmill_Raspi`
Then you need to install the other requirements by typing
`sudo apt-get install -r requirements.txt`.
If you have completed the hardware tasks you can start measuring by typing 
`python raspi_fildmill.py` or (preferred)
`python3 raspi_fieldmill.py`

##  Vision

If many people have contributed to our fieldmill project, we want to make a digital map, where you can see approximately the strength of the electric field on many locations. Through this we may approve finding the risk and development of thunderstorms.

##  Issues/Next steps

We want to implement an fft (fast furier transformation) to our code, so one can find out the frequency of the signal.

The README is to long. We want to make a longer documentation and short the README.
