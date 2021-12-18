import math

import cv2.cv2 as cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon = 0.5, trackCon = 0.5):
        #detector de la mano

        #Parametros para mediapipe
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon


        #Mediapipe se encarga de detectar las manos
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        #Para dibujar las landmarks de los puntos que entrega mediapipe
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):

        #A partir de la informacion que se recibe de mediapipe se dibujan las manos detectadas
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)


        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img


    def findPosition(self, img, handNo=0, draw=False ):
        #Se retornan las posciones en la imagen de cada una de las posiciones de la mano
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id,cx,cy, lm.z])

                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255 , 100), cv2.FILLED)
        return lmList


def distance_points(lmList, id1 , id2):
    #encuentra la distancia de dos puntos de la mano
    pointx = (lmList[id1][1], lmList[id1][2])
    point1 = (lmList[id2][1], lmList[id2][2])
    return math.dist(point1, pointx)

def finger_open_list(lmList):
    #retorna una lista con los dedos que estan levantados
    fingers = [] # 0 = close , 1 = open thumb to pinkie
    t = [12, 16, 20]
    if not lmList:
        return
    #thumb no funciona taaaan bien
    if distance_points(lmList, 4, 9) > distance_points(lmList, 3, 9):
        fingers.append(1)
    else:
        fingers.append(0)
    #index
    if distance_points(lmList, 8, 1) > distance_points(lmList, 7, 1):
        fingers.append(1)
    else:
        fingers.append(0)
    #mid, anular, pinky
    for tip in t:
        if distance_points(lmList, tip, 0) > distance_points(lmList, tip-1, 0):
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

