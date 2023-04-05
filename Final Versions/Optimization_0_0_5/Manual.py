"""
This code is used to control the drone with the head movement. The QR-codes will automatically be detected and opened.
User interaction is needed to close the images.
"""

from djitellopy import Tello
from threading import Thread
from time import sleep
import MuseController as mc
import VideoManager as vm
import cv2

ANGLE = 90  #Rotation angle (degrees)
HEIGHT = 20 #Height differential value (centimeters)
FORWARD = 20 #FW and BW movement distance (centimeters)

def main():
    #Drone initialization
    my_drone = Tello()
    my_drone.connect()
    my_drone.streamon()

    c = 0 #Concentration value
    while c >= 1: #if the value goes above 1, the drone takes off
        print("----------------------------------------------------------------")
        c = mc.museConcentrazione()
        print("concentrazione: ", c)
        # Note: Streaming is synchronous, so code here will not execute until the stream has been closed

    #Takeoff
    my_drone.takeoff()

    k = 20 #Variable used to keep track of the height, initialized to 20 after takeoff
    prec = 0 #Variable used to save the previous gryo value, the drone mustn't move when the head goes back to its position

    #Video streaming thread initialization
    streaming = vm.VideoManager(my_drone)
    streaming.start()

    #Main loop
    while True:
        theta, gamma, alpha = mc.museDxSx() #gyro values

        if streaming.getImageViewed() is True: #The user has already viewed and closed the image, controls enabled
            #Height
            if gamma > mc.SX_GAMMA:
                my_drone.move_up(HEIGHT)
                k += HEIGHT
            elif gamma < mc.DX_GAMMA:
                if k > HEIGHT:
                    my_drone.move_down(HEIGHT)
                    k -= HEIGHT
                else: #if the drone is less than 20 cm from the ground we land it
                    my_drone.land()
                    break
            
            #Rotation
            if prec > mc.DX_THETA and prec < mc.SX_THETA:
                if theta > mc.SX_THETA:
                    my_drone.rotate_counter_clockwise(+ANGLE)
                    sleep(2)
                elif theta < mc.DX_THETA:
                    my_drone.rotate_counter_clockwise(-ANGLE)
                    sleep(2)
            prec = theta
            
            #FW and BW
            if alpha > mc.FW_ALPHA:
                my_drone.move_forward(FORWARD)
            elif alpha < mc.RW_ALPHA:
                my_drone.move_back(FORWARD)

    #Closing everything
    cv2.destroyAllWindows()
    my_drone.land()
    my_drone.streamoff()
    quit()

if __name__ == '__main__':
    main()