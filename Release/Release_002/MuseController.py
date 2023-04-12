#Muse2 Libraries
from muselsl import stream, list_muses
from pylsl import StreamInlet, resolve_byprop
import utils
import numpy as np

#Base concentration level
CONCENTRAZIONE = 1

#Variables for gyroscope
SX_GAMMA = 1.5

DX_GAMMA = -1.5

SX_THETA = 3

DX_THETA = -3

FW_ALPHA = 1.5

RW_ALPHA = -1.5

#Streaming buffer lenght
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

streams_Gyro = resolve_byprop('type', 'Gyroscope', timeout=2) #start gyroscope
#creare un'altra stream per EEG
streams_EEG = resolve_byprop('type', 'EEG', timeout=2) #start EEG signals, for concentration

#secondo inlet per EEG
inlet_Gyro = StreamInlet(streams_Gyro[0], max_chunklen=12) 
info_Gyro = inlet_Gyro.info()

inlet_EEG = StreamInlet(streams_EEG[0], max_chunklen=12)
info_EEG  = inlet_EEG.info()  

fs_Gyro = int(info_Gyro.nominal_srate()) #gyro data frequency
#fs2 per EEGf
fs_EEG = int(info_EEG.nominal_srate()) #EEG data frequency

def museDxSx():
    # Obtain EEG data from the LSL stream
    gyro_data, timestamp = inlet_Gyro.pull_chunk(
    timeout=1, max_samples=int(SHIFT_LENGTH * fs_Gyro))
    
    theta = 0.2 * (gyro_data[-1][2] + gyro_data[-2][2] + gyro_data[-3][2] + gyro_data[-4][2] + gyro_data[-5][2]) * 1 / fs_Gyro #velocita in questo istante, media degli ultimi 2 valori, per giroscopio
    
    gamma = 0.2 * (gyro_data[-1][0] + gyro_data[-2][0] + gyro_data[-3][0] + gyro_data[-4][0] + gyro_data[-5][0]) * 1 / fs_Gyro

    alpha = 0.2 * (gyro_data[-1][1] + gyro_data[-2][1] + gyro_data[-3][1] + gyro_data[-4][1] + gyro_data[-5][1]) * 1 / fs_Gyro
    
    #theta = head rotation dx e sx
    #gamma = side tilt dx e sx
    #alpha = fw and rw tilt
    
    return theta, gamma, alpha #Data for the movement of the drone

def museConcentrazione():
    eeg_buffer = np.zeros((int(fs_EEG * BUFFER_LENGTH), 1))
    filter_state = None  # for use with the notch filter
    EEG_data, timestamp = inlet_EEG.pull_chunk(
        timeout=1, max_samples=int(SHIFT_LENGTH * fs_EEG))
    ch_data = np.array(EEG_data)[:, INDEX_CHANNEL]
    eeg_buffer, filter_state = utils.update_buffer(eeg_buffer, ch_data, notch=True, filter_state=filter_state)

    """ 3.2 COMPUTE BAND POWERS """
    data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs_EEG)
    band_powers = utils.compute_band_powers(data_epoch, fs_EEG) #band_powers(raggi alpha, beta, theta, delta) every EEG
    #print (band_powers)
    band_beta = utils.compute_beta(data_epoch, fs_EEG)
    
    return band_beta #get concentration value