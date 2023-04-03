from threading import Thread
from time import sleep

import urllib.request
import cv2
import numpy as np

class VideoManager(Thread):
    def __init__(self,my_drone):
        self.drone = my_drone
        self.detector = cv2.QRCodeDetector()
        self.imageViewed = True
        Thread.__init__(self)
    
    def run(self):
        while True:
            frame = self.drone.get_frame_read().frame
            try:
                data, _, _ = self.detector.detectAndDecode(frame)
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
            self.drone.land()
            self.drone.streamoff()
            quit()
        except:
            quit()

    def getImageViewed(self):
        return self.imageViewed