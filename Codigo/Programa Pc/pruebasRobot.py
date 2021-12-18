import time
import concurrent.futures
import apuntar
from send_angles import ConectarRaspy




def main():
    #Detección de la mano
    dedos = apuntar.DirectionsFingers()
    #Conexión a la raspi
    mensaje = ConectarRaspy()


    def loop_mensaje():
        #loop para mandar la dirección a la raspi
        #Se manda el mensaje solo si es distinto al anterior
        pDir = "stop"
        while True:
            cDir = dedos.direccion
            if cDir == pDir:
                if cDir == "leave":
                    #Se detiene si recibe el comando "leave"
                    break
                pDir = cDir
                time.sleep(.1)
                continue
            else:
                mensaje.mandar_direccion(cDir)
                if cDir == "leave":
                    print("Ya no se mueve")
            pDir = cDir
            time.sleep(.1)

        #Se termina la conexión al raspi
        mensaje.close()


    with concurrent.futures.ThreadPoolExecutor() as executor:
        #2 threads, uno encargado de la detección de los dedos
        f1 = executor.submit(dedos.capturar)
        # y otro de mandar las direcciones a la raspi
        loop_mensaje()

if __name__ == '__main__':
    main()