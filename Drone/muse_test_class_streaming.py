"""
Starting a Stream

This example shows how to search for available Muses and
create a new stream
"""
#FUNZIONAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
"""Idea Serra: delay se non muove la testa -> sla -> fermo"""
#Librerie muse2
from muselsl import stream, list_muses
from pylsl import StreamInlet, resolve_byprop
import utils
import time
import numpy as np

#Librerie drone
from djitellopy import Tello
import cv2

#Streaming video
import video_streaming

#Thread
from threading import Thread

from time import sleep

#Angle
ANGLE = 90  #90 verso sx

#Livello base di concentrazione
CONCENTRAZIONE = 6

SX_GAMMA = 1.5 #Giroscopio gamma orientato a sinistra se > 0.5

DX_GAMMA = -1.5 #Giroscopio gamma orientato a destra se < -0.5

SX_THETA = 3 #Giroscopio theta orientato a sinistra se < -0.5

DX_THETA = -3 #Giroscopio theta orientato a destra se < -0.5

FW_ALPHA = 1.5 #Giroscopio alpha orientato diritto se < -0.5

RW_ALPHA = -1.5 #Giroscopio alpha orientato indietro se < -0.5

HEIGHT = 20 #Valore di innalzamento o abbassamento drone

FORWARD = 20 #Valore di avanzamento o indietreggiamento drone

BUFFER_LENGTH = 5

# Length of the epochs used to compute the FFT (in seconds)
EPOCH_LENGTH = 1

# Amount of overlap between two consecutive epochs (in seconds)
OVERLAP_LENGTH = 0.8

# Amount to 'shift' the start of each next consecutive epoch
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

# Index of the channel(s) (electrodes) to be used
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
INDEX_CHANNEL = [0]

stream("00:55:da:b5:4a:32", ppg_enabled=True, acc_enabled=True, gyro_enabled=True) #"00:55:da:b5:49:3e" = MAC ADDRESS MUSE 2

streams_Gyro = resolve_byprop('type', 'Gyroscope', timeout=2) #fa partire il giroscopio
#creare un'altra stream per EEG
streams_EEG = resolve_byprop('type', 'EEG', timeout=2) #fa partire i segnali EEG, che servono per trovare la concentrazione

#secondo inlet per EEG
inlet_Gyro = StreamInlet(streams_Gyro[0], max_chunklen=12) 
info_Gyro = inlet_Gyro.info()

inlet_EEG = StreamInlet(streams_EEG[0], max_chunklen=12)
info_EEG  = inlet_EEG.info()  

fs_Gyro = int(info_Gyro.nominal_srate()) #frequenza del giroscopio
#fs2 per EEG
fs_EEG = int(info_EEG.nominal_srate()) #frequenza segnali EEG

#Inzializzazione drone
my_drone = Tello()
my_drone.connect()
my_drone.streamon()

def museDxSx():
    # Obtain EEG data from the LSL stream
    gyro_data, timestamp = inlet_Gyro.pull_chunk(
    timeout=1, max_samples=int(SHIFT_LENGTH * fs_Gyro))
    
    theta = 0.2 * (gyro_data[-1][2] + gyro_data[-2][2] + gyro_data[-3][2] + gyro_data[-4][2] + gyro_data[-5][2]) * 1 / fs_Gyro #velocita in questo istante, media degli ultimi 2 valori, per giroscopio
    
    gamma = 0.2 * (gyro_data[-1][0] + gyro_data[-2][0] + gyro_data[-3][0] + gyro_data[-4][0] + gyro_data[-5][0]) * 1 / fs_Gyro

    alpha = 0.2 * (gyro_data[-1][1] + gyro_data[-2][1] + gyro_data[-3][1] + gyro_data[-4][1] + gyro_data[-5][1]) * 1 / fs_Gyro
    
    #gamma = inclinazione testa dx e sx
    #theta = rotazione testa dx e sx
    #alpha = inclinazione avanti e indietro
    
    return theta, gamma, alpha #Vengono inviati due dati al drone

def museConcentrazione(): #restituisce il comando in entrata  per la concentrazione
    eeg_buffer = np.zeros((int(fs_EEG * BUFFER_LENGTH), 1))
    filter_state = None  # for use with the notch filter
    EEG_data, timestamp = inlet_EEG.pull_chunk(
        timeout=1, max_samples=int(SHIFT_LENGTH * fs_EEG))
    ch_data = np.array(EEG_data)[:, INDEX_CHANNEL]
    eeg_buffer, filter_state = utils.update_buffer(eeg_buffer, ch_data, notch=True, filter_state=filter_state)

    """ 3.2 COMPUTE BAND POWERS """
    data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs_EEG)
    band_powers = utils.compute_band_powers(data_epoch, fs_EEG) #band_powers(raggi alpha, beta, theta, delta) cioè tutti gli EEG
    #print (band_powers)
    band_beta = utils.compute_beta(data_epoch, fs_EEG) #compute_beta funzione per il calcolo dei raggi beta(concentrazione)
    
    return band_beta #Restituisce il valore della concentrazione

class Process(Thread):      #Gestisce i movimenti
    def __init__(self, tello):
        Thread.__init__(self)
        self.tello = tello
       
    def run(self):
        while True:
            frame = self.tello.get_frame_read().frame
            frame = cv2.resize(frame, (720, 480))
            cv2.imshow("video", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27: #ESC
                break
            sleep(0.02)
        self.tello.streamoff()
        cv2.destroyAllWindows()
        quit()

if __name__ == "__main__":
    while True:
        print("----------------------------------------------------------------")
        c = museConcentrazione()
        print("concentrazione: ", c)
        # Note: Streaming is synchronous, so code here will not execute until the stream has been closed
        if c >= 1:  break
    #Decollo
    my_drone.takeoff()
    k = 0
    prec = 0
    straming = Process(my_drone)
    straming.start()
    while True:
        theta, gamma, alpha = museDxSx()

        if True == True:
            #print("Comandi attivabili")
            if gamma > SX_GAMMA:   #FUNZIONA!!!
                my_drone.move_up(HEIGHT)
                k += HEIGHT
            elif gamma < DX_GAMMA:
                if k > HEIGHT:
                    my_drone.move_down(HEIGHT)
                    k -= HEIGHT
                else: 
                    my_drone.land()
                    break
            
            #print(f"theta = {theta}")    #VERSIONE DA TESTARE - 29/03/23
            #print(f"prec = {prec}")
            if prec > DX_THETA and prec < SX_THETA:
                if theta > SX_THETA:
                    my_drone.rotate_counter_clockwise(+ANGLE)
                    k += 1
                    sleep(2)
                elif theta < DX_THETA:
                    my_drone.rotate_counter_clockwise(-ANGLE)
                    k += 1
                    sleep(2)
            prec = theta
            
            #print(alpha)     #FUNZIONA!!!
            if alpha > FW_ALPHA:
                my_drone.move_forward(FORWARD)
                k += 1
            elif alpha < RW_ALPHA:
                my_drone.move_back(FORWARD)
                k += 1
