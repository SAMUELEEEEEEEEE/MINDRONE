"""
This code is used when the user is unable to move his neck. The drone will follow a predefined route and stop to open the QR-Codes.
The images will be closed when the user stops focusing.
"""

from djitellopy import Tello
from time import sleep
import VideoManager as vm
    
def main():
    #Drone setup
    my_drone = Tello()
    my_drone.connect()
    my_drone.streamon() 
    my_drone.takeoff()

    #Video thread setup
    video = vm.VideoManager(my_drone)
    video.start()
    sleep(10)
    
    #Pylon 1, verify if the user already viewed the image in order to prevent the drone from moving
    while video.getImageViewed() == False:
        pass

    #Move to pylon 2
    my_drone.rotate_counter_clockwise(90)
    my_drone.move_forward(190)
    my_drone.rotate_counter_clockwise(-90)
    
    #Pylon 2, verify if the user already viewed the image in order to prevent the drone from moving
    sleep(0.5)
    while video.getImageViewed() == False:
        pass

    #Move to pylon 3
    my_drone.rotate_counter_clockwise(180)
    my_drone.move_forward(130)
    
    #Pylon 3, verify if the user already viewed the image in order to prevent the drone from moving
    sleep(0.5)
    while video.getImageViewed() == False:
        pass
    
    #Move to pylon 4
    my_drone.rotate_counter_clockwise(90)
    my_drone.move_forward(165)
    my_drone.rotate_counter_clockwise(-90)
    
    #Pylon 4, verify if the user already viewed the image in order to prevent the drone from moving
    sleep(0.5)
    while video.getImageViewed() == False:
        pass

    #Return home
    my_drone.rotate_counter_clockwise(180)
    my_drone.move_forward(135)
    my_drone.land()

if __name__ =="__main__":
    main()