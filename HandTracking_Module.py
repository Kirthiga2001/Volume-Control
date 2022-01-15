import mediapipe as mp
import cv2
import time

class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.drawingdetails = mp.solutions.drawing_utils
        self.mphand = mp.solutions.hands
        self.hands = self.mphand.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)

    def findHands(self,frame,draw=True):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(rgb)
        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                if draw:
                    self.drawingdetails.draw_landmarks(frame, handlms, self.mphand.HAND_CONNECTIONS)
        return frame

    def findPosition(self,frame,handNumber,draw=True):
        lmList=[]
        if self.result.multi_hand_landmarks:
                handlms=self.result.multi_hand_landmarks[handNumber]
                for id, lm in enumerate(handlms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id,cx,cy])
                    if draw:
                        cv2.circle(frame, (cx, cy), 50, (255, 255, 0), 10)
        return lmList



def main():
    cap = cv2.VideoCapture(0)
    ptime, ctime = 0, 0
    detector =handDetector()
    while 1:
        t, frame = cap.read()
        frame=detector.findHands(frame)
        lmlist=detector.findPosition(frame,0)
        print(lmlist)
        ctime = time.time()
        fps = int(1 // (ctime - ptime))
        ptime = ctime

        cv2.putText(frame, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Video", frame)
        cv2.waitKey(1)

if __name__=="__main__":
    main()