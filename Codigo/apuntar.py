import cv2.cv2 as cv2
import time
import HandTrackingModule as htm


class DirectionsFingers:

    def __init__(self):

        #Se inicia la camara
        #########################
        self.wCam, self.hCam = 640, 480
        ##########################

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)


        self.direccion = "stop"

        #se inicia el detector de la mano
        self.detector = htm.handDetector(detectionCon=0.7)


    def capturar(self):
        pTime = 0
        prev_dir = "stop"
        counter = 0

        #la camra toma un frame y luego se decide que comando mandar
        while True:
            #Se toma el frame
            success, img = self.cap.read()
            img = cv2.flip(img, 2)
            #se detectan las manos
            img = self.detector.findHands(img)
            #se encuentra la lista con las posiciones de la mano
            lmList = self.detector.findPosition(img, draw=False)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            #si se hace una pistola con la mano, se decide adonde está apuntando, dependiendo de donde apunta, la direccion que se escoge.
            if htm.finger_open_list(lmList) == [1, 1, 0, 0, 0]:
                index_tip = (lmList[8][1],lmList[8][2])
                thumb_base = (lmList[1][1], lmList[1][2])
                cv2.line(img,index_tip, thumb_base, (0,0,255), 5)
                if abs(index_tip[0] - thumb_base[0]) > abs(index_tip[1] - thumb_base[1]):
                    if index_tip[0] - thumb_base[0] > 0:
                        cur_dir ="right"
                    else:
                        cur_dir = "left"
                else:
                    if index_tip[1] - thumb_base[1] > 0:
                        cur_dir ="down"
                    else:
                        cur_dir = "up"

            #si se levante le pulgar y meñique la direccion es hacia adelante
            elif htm.finger_open_list(lmList) == [1, 0, 0, 0, 1]:
                cur_dir = "front"
            # si se levante el pulgar, indice y meñique la direccion es hacia atras
            elif htm.finger_open_list(lmList) == [1, 1, 0, 0, 1]:
                cur_dir = "back"
            # si se levante el pulgar y dedo medio la direccion es salir
            elif htm.finger_open_list(lmList) == [1, 0, 1, 0, 0]:
                cur_dir = "leave"
            # si se levante el pulgar, indice y dedo medio la direccion es abrir
            elif htm.finger_open_list(lmList) == [1,1,1,0,0]:
                cur_dir = "abrir"
            # si se levante el pulgar, indice, dedo medio y anular la direccion es cerrar
            elif htm.finger_open_list(lmList) == [1,1,1,1,0]:
                cur_dir = "cerrar"

            #si no es un comando conocido, la dirección es quieto
            else:
                cur_dir = "stop"


            ## Arreglar errores de precision (la direccion tiene que ser igual algunos frames para cambiar.)
            if counter != 1:
                if prev_dir == cur_dir:
                    counter += 1
                else:
                    counter = 0
            else:
                if prev_dir != cur_dir:
                    counter = 0
                else:
                    self.direccion = cur_dir

            prev_dir = cur_dir

            #escribimos los fps en la imagen
            cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

            #Muestra la imagen con los fps y las marcas de las manos
            cv2.imshow("Image", img)


            # Se detiene la detección si se apreta la tecla "q".
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    dedos = DirectionsFingers()
    dedos.capturar()
