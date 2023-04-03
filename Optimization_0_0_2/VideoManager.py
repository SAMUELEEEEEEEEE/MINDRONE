from threading import Thread
from time import sleep

import urllib.request
import cv2
import numpy as np
from final_GUI import GUI

#Associate each link to a short description, displayed in the GUI
descriptions = {
    "https://cdn.studenti.stbm.it/images/2017/01/10/gioconda-orig.jpeg" : "The Mona Lisa, also known as Mona Lisa, is an oil painting on poplar table made by Leonardo da Vinci (77 × 53 cm and 13 mm thick), dated to about 1503-1506 and preserved in the Louvre Museum in Paris.",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/The_Rape_of_Proserpina_%28Rome%29.jpg/217px-The_Rape_of_Proserpina_%28Rome%29.jpg" : "The Rape of Proserpina is a sculptural group made by Gian Lorenzo Bernini, performed between 1621 and 1622 and exhibited in the Galleria Borghese in Rome.",
    "https://www.theartpostblog.com/wp-content/uploads/2017/05/img-notte-stellata-van-gogh.jpg" : "The Starry Night (De sterrennacht) is a painting by the Dutch painter Vincent van Gogh, made in 1889 and preserved at the Museum of Modern Art in New York. A true icon of Western painting, the painting depicts a nocturnal landscape of Saint-Rémy-de-Provence, just before sunrise.",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Michelangelo%27s_David_-_right_view_2.jpg/1200px-Michelangelo%27s_David_-_right_view_2.jpg" : "David is a masterpiece of Renaissance sculpture, created in marble between 1501 and 1504 by the Italian artist Michelangelo. David is a 5.17-metre (17 ft 0 in) marble statue of the Biblical figure David, a favoured subject in the art of Florence."
}

class VideoManager(Thread):
    def __init__(self,my_drone):
        self.drone = my_drone
        self.detector = cv2.QRCodeDetector()
        self.imageViewed = True
        self.gui = GUI()
        Thread.__init__(self)
        
    
    def run(self):
        while True:
            frame = self.drone.get_frame_read().frame
            try:
                data, _, _ = self.detector.detectAndDecode(frame)
                # check if there is a QRCode in the image
                if data:
                    self.imageViewed = False
                    a=data
                    #print(str(a))
                    req = urllib.request.urlopen(str(a))
                    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                    img = cv2.imdecode(arr, -1) # 'Load it as it is
                    img = cv2.resize(img, (360, 500))
                    cv2.imshow("img", img)
                    cv2.imshow("video", frame)
                    global descriptions
                    self.gui.updateDescription(descriptions[str(a)])
                    while(cv2.waitKey(1) & 0xFF != ord('e')):
                        pass

                    self.imageViewed = True
                    cv2.destroyWindow("img")
                    self.gui.updateDescription('')
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