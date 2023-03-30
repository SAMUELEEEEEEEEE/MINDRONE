from djitellopy import Tello
import cv2
from time import sleep
from threading import Thread

my_drone = Tello()
my_drone.connect() #rileva il drone nella rete solo se e' la stessa
my_drone.streamon() 

class Movimento(Thread):
    def __init__(self,my_drone):
        self.drone = my_drone
        Thread.__init__(self)
    
    def run(self):
        while True:
            frame = self.drone.get_frame_read().frame
            frame = cv2.resize(frame, (720, 480))
            cv2.imshow('video', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27: #esc
                break
        my_drone.land()
        my_drone.streamoff()
        cv2.destroyAllWindows()
        quit()
        

def main():
    my_drone.takeoff() #accensione motori
    drone = Movimento(my_drone)
    drone.start()
    sleep(5)

    my_drone.rotate_counter_clockwise(90)#rotazione per anadre dal 2 pilastro
    my_drone.move_forward(195)#da 1 pilastro a 2 pilastro
    my_drone.rotate_counter_clockwise(-90) #facca faccia col qr code del 2 pilastro
    
    my_drone.rotate_counter_clockwise(180)#rotazione per anadre dal 3 pilastro
    my_drone.move_forward(150)#da 2 pilastro a 3 pilastro

    my_drone.rotate_counter_clockwise(90)#rotazione per anadre dal 4 pilastro
    my_drone.move_forward(179)#da 3 pilastro a 4 pilastro
    my_drone.rotate_counter_clockwise(-90) #facca faccia col qr code del 4 pilastro

    my_drone.rotate_counter_clockwise(180)#rotazione per anadre dal 1 pilastro
    my_drone.move_forward(150)#da 4 pilastro a 1 pilastro
    my_drone.land()

#connettere il drone sulla nostra stessa rete

if __name__ =="__main__":
    main()