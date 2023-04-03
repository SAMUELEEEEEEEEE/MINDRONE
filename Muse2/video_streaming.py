from djitellopy import Tello
import cv2

def video_stream(my_drone):
    frame = my_drone.get_frame_read().frame
    frame = cv2.resize(frame, (360, 240))
    cv2.imshow("video", frame)
    if cv2.waitKey(5) & 0XFF == 27: 
        pass
    #cv2.waitKey(0)
    return #cv2.getWindowProperty("video", cv2.WND_PROP_VISIBLE)