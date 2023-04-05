from threading import Thread
from time import sleep

import urllib.request
import cv2
import time
import numpy as np

class VideoManager(Thread):
    def __init__(self,my_drone):
        self.drone = my_drone
        self.detector = cv2.QRCodeDetector()
        self.imageViewed = True #Used to lock and unlock the controls
        Thread.__init__(self)
    
    def run(self):
        #Keep track of the already opened images and to prevent them to be showed again
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
                    #Open the link, show the image in a cv2 window
                    self.imageViewed = False
                    a = str(data)
                    req = urllib.request.urlopen(a)
                    arr = np.asarray(bytearray(req.read()), dtype = np.uint8)
                    img = cv2.imdecode(arr, -1) # 'Load it as it is
                    img = cv2.resize(img, (360, 500))
                    cv2.imshow("img", img)
                    start_time = time.time()
                    current_time = time.time()
                    while current_time - start_time <  5:
                        cv2.imshow("video", frame) #keep showing the video
                        current_time = time.time()

                    #Unlock the controls, set the image to opened to prevent it from reopening
                    self.imageViewed = True
                    dic[str(data)] = True
                    #Close the image
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