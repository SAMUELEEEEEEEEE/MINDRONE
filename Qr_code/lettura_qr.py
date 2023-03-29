import glob
import cv2
import urllib.request
import numpy as np
import pandas as pd
import pathlib

def read_qr_code(filename):
    """Read an image and read the QR code.
    
    Args:
        filename (string): Path to file
    
    Returns:
        qr (string): Value from QR code
    """
    
    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value
    except:
        return
    
value = read_qr_code('qrcode_cdn.studenti.stbm.it.png')

print(value)

req = urllib.request.urlopen(value)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1) # 'Load it as it is'

cv2.imshow('random_title', img)
if cv2.waitKey() & 0xff == 27: quit()
