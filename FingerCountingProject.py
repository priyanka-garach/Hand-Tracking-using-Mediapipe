import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 640

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

overlayList = []

pTime = 0         #previous time

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print("lmlist")
    #print(lmList)

    # CODE FOR 1st FINGER
     # if len(lmList) != 0:
     #     fingers = []
     #     if lmList[8][2] < lmList[6][2]:
     #         print("Index finger open ")

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        #h, w, c = overlayList[totalFingers].shape
        #img[0:h, 0:w] = overlayList[totalFingers]

        #cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 175), cv2.FONT_HERSHEY_PLAIN,
                    10, (139, 0, 139), 25)


    cTime = time.time()   #current time
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                1, (255, 0, 139), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)