"""
This code is used when the user is unable to move his neck. The drone will follow a predefined route and stop to open the QR-Codes.
The images will be closed when the user stops focusing.
"""

from djitellopy import Tello
from time import sleep
import numpy as np
import VideoManager as vm
    
def main():
    my_drone = Tello()
    my_drone.connect() #The drone can be connected only if it is in the same network
    my_drone.streamon() 
    my_drone.takeoff() #accensione motori, qr 1 pilastro
    video = vm.VideoManager(my_drone)
    video.start()
    sleep(10)
    
    while video.getImageViewed() == False:
        pass

    my_drone.rotate_counter_clockwise(90)#rotazione per anadre dal 2 pilastro
    my_drone.move_forward(190)#da 1 pilastro a 2 pilastro
    my_drone.rotate_counter_clockwise(-90) #facca faccia col qr code del 2 pilastro
    
    sleep(0.5)
    while video.getImageViewed() == False:
        pass

    my_drone.rotate_counter_clockwise(180)#rotazione per anadre dal 3 pilastro
    my_drone.move_forward(130)#da 2 pilastro a 3 pilastro
    
    sleep(0.5)
    while video.getImageViewed() == False:
        pass
    
    my_drone.rotate_counter_clockwise(90)#rotazione per anadre dal 4 pilastro
    my_drone.move_forward(165)#da 3 pilastro a 4 pilastro
    my_drone.rotate_counter_clockwise(-90) #facca faccia col qr code del 4 pilastro
    
    sleep(0.5)
    while video.getImageViewed() == False:
        pass

    my_drone.rotate_counter_clockwise(180)#rotazione per anadre dal 1 pilastro
    my_drone.move_forward(135)#da 4 pilastro a 1 pilastro
    my_drone.land()

if __name__ =="__main__":
    main()