
# Rest of your TensorFlow code
import random
from turtle import delay
from unittest import result
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

#import tensorflow as tf

import os
os.environ['TF_ENABLE_OEDNN_OPTS'] = '0'

class rock:
    def __init__(self):   
        cap = cv2.VideoCapture(0)  
        cap.set(3, 640)
        cap.set(4, 480)
        detector = HandDetector(maxHands=1)

        timer = 0
        stateResult = False
        startGame = False
        scores = [0, 0]  # [AI, Player]

        while True:
            imgBG = cv2.imread("Resources/BG.png")
            success, img = cap.read()
            if not success or img is None:
                print("Error: Failed to capture image")
                continue  
            imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
            imgScaled = imgScaled[:, 80:480]
            # Find Hands
            hands, img = detector.findHands(imgScaled)  # with draw
            if startGame:
                if stateResult is False:
                    timer = time.time() - initialTime
                    cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
                    if timer > 2:
                        stateResult = True
                        timer = 0
                        if hands:
                            playerMove = None
                            hand = hands[0]
                            fingers = detector.fingersUp(hand)
                            if fingers == [0, 0, 0, 0, 0]:
                                playerMove = 1
                            if fingers == [1, 1, 1, 1, 1]:
                                playerMove = 2
                            if fingers == [0, 1, 1, 0, 0]:
                                playerMove = 3
                
                            randomNumber = random.randint(1, 3)
                            imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                            imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                            # Player Wins
                            if (playerMove == 1 and randomNumber == 3) or \
                                    (playerMove == 2 and randomNumber == 1) or \
                                    (playerMove == 3 and randomNumber == 2):
                                scores[1] += 1  
                                
                            # AI Wins
                            if (playerMove == 3 and randomNumber == 1) or \
                                    (playerMove == 1 and randomNumber == 2) or \
                                    (playerMove == 2 and randomNumber == 3):
                                scores[0] += 1

                            #draw
                            if (playerMove == 1 and randomNumber == 1) or \
                                    (playerMove == 2 and randomNumber == 2) or \
                                    (playerMove == 3 and randomNumber == 3):
                                scores[1] += 0     
                                scores[0] += 0    

            imgBG[234:654, 795:1195] = imgScaled
            if stateResult:
                imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
                if (playerMove == 1 and randomNumber == 3) or \
                                    (playerMove == 2 and randomNumber == 1) or \
                                    (playerMove == 3 and randomNumber == 2):
                    cv2.putText(imgBG, "Player Wins", (390, 430), cv2.FONT_HERSHEY_PLAIN, 6, (0,0,255), 9)
                if (playerMove == 3 and randomNumber == 1) or \
                                    (playerMove == 1 and randomNumber == 2) or \
                                    (playerMove == 2 and randomNumber == 3):
                    cv2.putText(imgBG, "AI Wins", (490, 430), cv2.FONT_HERSHEY_PLAIN, 6, (0,0,255), 9)
                if (playerMove == 1 and randomNumber == 1) or \
                                    (playerMove == 2 and randomNumber == 2) or \
                                    (playerMove == 3 and randomNumber == 3):
                    cv2.putText(imgBG, "DRAW", (515, 430), cv2.FONT_HERSHEY_PLAIN, 6, (0,0,255), 9)
            
                
            cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
            cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

            cv2.putText(imgBG, "For Reset the game -> press 'r'", (35, 700), cv2.FONT_HERSHEY_PLAIN, 2, (100, 100, 255), 3)
            cv2.putText(imgBG, "For Quit the game -> press 'q'", (715, 700), cv2.FONT_HERSHEY_PLAIN, 2, (100, 100, 255), 3)
        
            cv2.imshow("ROCK-PAPER-SCISSOR", imgBG)

            key = cv2.waitKey(1)
            if key == ord('r'):
            
            # while key!= ord('q'): 
            
                startGame = True
                initialTime = time.time()
                stateResult = False
        
            if key == ord('q'):
                cv2.destroyAllWindows() 
                break