import cv2
import urllib.request
import numpy as np

cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()


while True:
    _, img = cap.read()
    # detect and decode
    try:
        data, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if data:
            a=data
            break
        cv2.imshow("QRCODEscanner", img)    
        if cv2.waitKey(1) == ord("q"):
            break
    except:
        pass
  
cap.release()
req = urllib.request.urlopen(str(a))
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1) # 'Load it as it is'

cv2.imshow('QRCODEscanner', img)
if cv2.waitKey() & 0xff == 27: quit()