from djitellopy import Tello
import cv2
import urllib.request
import numpy as np
from time import sleep

cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

while True:
    _, frame = cap.read()
    try:
        data, bbox, _ = detector.detectAndDecode(frame)
        # check if there is a QRCode in the image
        if data:
            a=data
            """req = urllib.request.urlopen(str(a))
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1) # 'Load it as it is'"""
            img = cv2.imread('.\Test_qr.jpeg')
            img = cv2.resize(img, (360, 500))
            cv2.imshow('QRCODEscanner', img)
            cv2.waitKey(0)
        cv2.imshow("QRCODEscanner", frame)    
    except:
        pass

    key = cv2.waitKey(1) & 0xFF
    if key == ord('w'):
        print('Avanti 20')
    elif key == ord('s'):
        print('Indietro 30')
    elif key == ord('a'):
        print('Sinistra 90')
    elif key == ord('d'):
        print('Destra 90')
    elif key == ord('l'):
        print('Atterraggio')
        cap.release()
        cv2.destroyAllWindows()
        quit()
    elif key == ord('u'):
        print('Su 20')
    elif key == ord('i'):
        print('Giu 20')