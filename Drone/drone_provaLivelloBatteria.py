from djitellopy import Tello
import cv2

#connettere il drone sulla nostra stessa rete
my_drone = Tello()
my_drone.connect() #rileva il drone nella rete solo se e' la stessa
my_drone.takeoff() #accensione motori

my_drone.move_forward(50)
my_drone.move_back(50)
my_drone.rotate_counter_clockwise(90)
my_drone.land() #atteraggio"""
battery_status = my_drone.get_battery()
print(f'livello batteria = {battery_status}')


 