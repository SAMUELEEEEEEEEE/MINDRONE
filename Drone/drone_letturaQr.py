from djitellopy import Tello
import cv2

#connettere il drone sulla nostra stessa rete
my_drone = Tello()
my_drone.connect() #rileva il drone nella rete solo se e' la stessa
detector = cv2.QRCodeDetector()

"""my_drone.move_forward(50)
my_drone.move_back(50)
my_drone.rotate_counter_clockwise(90)
my_drone.land() #atteraggio"""
battery_status = my_drone.get_battery()


my_drone.streamon()
my_drone.takeoff() #accensione motori

while True:
    _, frame = my_drone.get_frame_read().frame
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
        my_drone.move_forward(20)#cm
    elif key == ord('s'):
        my_drone.move_back(30)
    elif key == ord('a'):
        my_drone.rotate_counter_clockwise(-90)
    elif key == ord('d'):
        my_drone.rotate_counter_clockwise(90)
    elif key == ord('l'):
        my_drone.land()
    elif key == ord('u'):
        my_drone.move_up(20) 
    elif key == ord('i'):
        my_drone.move_down(20)