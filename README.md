# PROJECT AND GROUP DESCRIPTION
Our project is thought for people suffering from ALS (Amyotrophic Lateral Sclerosis) or multiple sclerosis and allow them to visit museums directly from their home through a drone called Tello. For people suffering from ASL that, in most cases, in advanced states of the disease, the patient can't move any muscle. He can continue to use the power of the brain concentration and we catch brain waves through a device called Muse2. After receiving a minimum signal of concentration, the drone rises and follows a pre-set path, in which it scans the qr code and shows the corresponding image of a certain artistic work. While, if users are people suffering from multiple sclerosis and they can move neck muscles, they can activate a second mode based on the movements of the neck to manage the direction of the drone in museums. It's been everything done through python.

Our group is composed of five members: Giraudo Giacomo, Leardi Ludovico, Menardi Samuele, Pellegrino Gabriele and Serra Alberto. At the beginning we choose the leader, Menardi Samuele, and subsequently we divided various tasks:

Menardi Samuele, the leader, who takes care of the organization of the work and coordination of the team in addition with Leardi to the study, development and programming of the sensor Muse2.

Giraudo Giacomo and Pellegrino Gabriele, drone managers, adduced to the development, study, and drone programming.

Serra Alberto, qr-code managers, adduced to the study and developmet about qr-codes.

# INSTRUCTIONS FOR USE
At the beginning, you have to click on this link and download all the folder: https://github.com/kowalej/BlueMuse , then must unzip this folder: https://github.com/kowalej/BlueMuse/blob/master/DistArchived/BlueMuse_2.0.0.0.zip

Enter in that folder and run : InstallBlueMuse.ps1 with PowerShell (you must activate developer mode from the pc settings).

Then you have to switch on the bluetooth on your pc and start the software of BlueMuse and click on "Start Streaming" and the Muse2 will start to recorder data.

Instead, to use Tello, you have to connect your device to Tello's wifi.


# LIBRARIES TO DOWNLOAD
To allow the project programs to work, you must install these libraries for python:

Write on terminal this string to download opencv library: pip install opencv-python

Write on terminal this string to download the library to control Tello drone: pip install djitellopy

Write on terminal this string to download the library: pip install numpy

Write on terminal this string to download the library fo python interface to the Lab Streaming Layer (LSL): pip install pylsl

The other libraries are already in python (es: time)

You must also download two folder and one file from this directory: 

Folders names: "muselsl" and "__ pycache__"

File name: "utils.py"


# FILES TO RUN
On the upper folder, Release, run the file Launcher.py
