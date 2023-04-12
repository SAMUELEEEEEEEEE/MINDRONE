"""
This program is used to choose the control mode. If the user doesn't move the head in 5 seconds the automatic mode will be used.
Otherwise, if the user moves the neck, the MUSE control mode will be used.
"""

import time

#Muse2 custom module
import MuseController as mc

#Main codes
import Manual
import Autopilot

if __name__ == '__main__':

    prec = 0 #Previous gyro value

    #Keep track of the time passed since the program started
    startTime = time.time()
    currentTime = time.time()
    moved = False

    print('Choose control mode (if you don\'t move your head for 5 seconds autopilot will launch)')

    while currentTime - startTime <= 5 and moved is False: #5 seconds have passed or the user moved the head

        theta, gamma, alpha = mc.museDxSx() #get gyro data from muse

        if gamma > mc.SX_GAMMA or gamma < mc.DX_GAMMA:
            moved = True
        
        if prec > mc.DX_THETA and prec < mc.SX_THETA:
            if theta > mc.SX_THETA or theta < mc.DX_THETA:
                moved = True
        prec = theta
        
        if alpha > mc.FW_ALPHA or alpha < mc.RW_ALPHA:
            moved = True
        
        currentTime = time.time()

    if moved is True: #The user is able to move his neck
        print('Launching control mode...')
        Manual.main()

    else:
        print('Launching auto mode...')
        Autopilot.main()
