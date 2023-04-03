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
        dic = {"https://cdn.studenti.stbm.it/images/2017/01/10/gioconda-orig.jpeg" : False,
                   "https://www.theartpostblog.com/wp-content/uploads/2017/05/img-notte-stellata-van-gogh.jpg" : False,
                   "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/The_Rape_of_Proserpina_%28Rome%29.jpg/217px-The_Rape_of_Proserpina_%28Rome%29.jpg" : False,
                   "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Michelangelo%27s_David_-_right_view_2.jpg/1200px-Michelangelo%27s_David_-_right_view_2.jpg" : False}
        
        while True:
            frame = self.drone.get_frame_read().frame
            try:
                data, _, _ = self.detector.detectAndDecode(frame)
                # check if there is a QRCode in the image
                if data and dic[str(data)] is False :
                    self.imageViewed = False
                    a=data
                    #print(str(a))
                    req = urllib.request.urlopen(str(a))
                    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                    img = cv2.imdecode(arr, -1) # 'Load it as it is
                    img = cv2.resize(img, (360, 500))
                    cv2.imshow("img", img)
                    cv2.imshow("video", frame)
                    while(cv2.waitKey(1) & 0xFF != ord('e')):
                        pass

                    self.imageViewed = True
                    dic[str(data)] = True
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