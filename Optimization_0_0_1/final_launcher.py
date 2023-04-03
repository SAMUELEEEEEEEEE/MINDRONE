"""
This program is used to choose the control mode. If the user doesn't move the head in 5 seconds the automatic mode will be used.
Otherwise, if the user moves the neck, the MUSE control mode will be used.
"""

import time

#Muse2 custom module
import MuseControl as mc

#Main codes
import final_muse
import final_auto

if __name__ == '__main__':
    theta, gamma, alpha = mc.museDxSx()

    startTime = time.time()
    currentTime = time.time()
    moved = False

    while currentTime - startTime <= 5000 and moved is False:
        if gamma > mc.SX_GAMMA or gamma < mc.DX_GAMMA:   #FUNZIONA!!!
            moved = True
        
        if prec > mc.DX_THETA and prec < mc.SX_THETA:
            if theta > mc.SX_THETA or theta < mc.DX_THETA:
                moved = True
        prec = theta
        
        #print(alpha)     #FUNZIONA!!!
        if alpha > mc.FW_ALPHA or alpha < mc.RW_ALPHA:
            moved = True

    if moved is True: #The user is able to move his neck
        print('Launching control mode...')

    else:
        print('Launching auto mode...')
        final_auto.main()
