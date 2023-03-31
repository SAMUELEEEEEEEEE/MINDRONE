from djitellopy import Tello
import cv2
from time import sleep
from threading import Thread
import urllib.request
import numpy as np

my_drone = Tello()
my_drone.connect() #rileva il drone nella rete solo se e' la stessa
my_drone.streamon() 
detector = cv2.QRCodeDetector()
imageViewed = True

class Movimento(Thread):
    def __init__(self,my_drone):
        self.drone = my_drone
        Thread.__init__(self)
    
    def run(self):
        while True:
            frame = my_drone.get_frame_read().frame
            try:
                data, _, _ = detector.detectAndDecode(frame)
                # check if there is a QRCode in the image
                if data:
                    global imageViewed
                    imageViewed = False
                    a=data
                    #print(str(a))
                    req = urllib.request.urlopen(str(a))
                    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                    img = cv2.imdecode(arr, -1) # 'Load it as it is
                    img = cv2.resize(img, (360, 500))
                    cv2.imshow("img", img)
                    cv2.imshow("video", frame)
                    print("immagine riprodotta")
                    while(cv2.waitKey(1) & 0xFF != ord('e')):
                        pass

                    imageViewed = True
                    cv2.destroyWindow("img")
                    sleep(1)
                cv2.imshow("video", frame)
            except:
                pass
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27: #esc
                break
        
        try:
            cv2.destroyAllWindows()
            my_drone.land()
            my_drone.streamoff()
            quit()
        except:
            quit()
    
def main():
    my_drone.takeoff() #accensione motori, qr 1 pilastro
    drone = Movimento(my_drone)
    drone.start()
    #print("start")
    sleep(10)
    
    while imageViewed == False:
        pass

    my_drone.rotate_counter_clockwise(90)#rotazione per anadre dal 2 pilastro
    my_drone.move_forward(190)#da 1 pilastro a 2 pilastro
    my_drone.rotate_counter_clockwise(-90) #facca faccia col qr code del 2 pilastro
    
    while imageViewed == False:
        pass

    my_drone.rotate_counter_clockwise(180)#rotazione per anadre dal 3 pilastro
    my_drone.move_forward(130)#da 2 pilastro a 3 pilastro
    
    while imageViewed == False:
        pass
    
    my_drone.rotate_counter_clockwise(90)#rotazione per anadre dal 4 pilastro
    my_drone.move_forward(165)#da 3 pilastro a 4 pilastro
    my_drone.rotate_counter_clockwise(-90) #facca faccia col qr code del 4 pilastro
    
    while imageViewed == False:
        pass

    my_drone.rotate_counter_clockwise(180)#rotazione per anadre dal 1 pilastro
    my_drone.move_forward(135)#da 4 pilastro a 1 pilastro
    my_drone.land()

#connettere il drone sulla nostra stessa rete

if __name__ =="__main__":
    main()