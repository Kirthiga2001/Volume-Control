import mediapipe as mp
import cv2
import time
import numpy as np
import HandTracking_Module as htm
import  math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
w,h=640,480;VOl_bar=0
cap = cv2.VideoCapture(0)
cap.set(3,w)
cap.set(4,h)
ptime, ctime = 0, 0
detector = htm.handDetector(detectionCon=0.8)

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
Min_vol,Max_Vol,s=volume.GetVolumeRange()

#(-95.25, 0.0, 0.75)

while 1:
    t, frame = cap.read()
    frame = detector.findHands(frame)
    lmlist = detector.findPosition(frame,0,draw=False)
    if lmlist:
        x1,y1=(lmlist[4][1],lmlist[4][2])
        x2, y2 = (lmlist[8][1], lmlist[8][2])
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(frame, (cx,cy), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(frame,(x1,y1),15,(255,0,0),cv2.FILLED)
        cv2.circle(frame, (x2, y2), 15, (255,0,0), cv2.FILLED)
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),5)
        d=math.hypot((x1-x2),(y1-y2))
        print(d)
        #hand=  10-200 to volumeRange
        vol=np.interp(d,[10,300],[Min_vol,Max_Vol])
        volume.SetMasterVolumeLevel(vol,None)
        VOl_bar=np.interp(vol,[Min_vol,Max_Vol],[0,250])
    cv2.rectangle(frame,(50,150),(85,400),(0,0,0),3)
    cv2.rectangle(frame, (50, 400-int(VOl_bar)), (85, 400), (0, 0, 0), cv2.FILLED)
    compVol=np.interp(VOl_bar,[0,250],[0,100])
    cv2.putText(frame, f'{int(compVol)}%', (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    ctime = time.time()
    fps = int(1 // (ctime - ptime))
    ptime = ctime

    cv2.putText(frame, f'FPS: {fps}', (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0,0), 3)

    cv2.imshow("Video", frame)
    cv2.waitKey(1)
