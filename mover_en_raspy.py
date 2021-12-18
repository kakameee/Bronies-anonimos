import sys
import time

sys.path.append('/home/pi/mlf/core')
from serial_control import SerialControl
from wait_comand import PedirDirecciones
import concurrent.futures

# LIMITES
# pose  0, 90
# pose2 40, 150
# pose3  60, 120


"""
#iniciales
pose = 45
pose2 = 90
pose3 = 90
speed = 2

direcciones = ["left", "right", "up", "down", "front", "back", "stop"]
"""


class Robot_posiciones:
    #Encargado de mover el robot y guardar sus posiciones.
    def __init__(self):
        #se inician las posiciones de lrobot
        self.pose = 45
        self.pose2 = 90
        self.pose3 = 90
        self.pose4 = 90
        #Cuanto se mueve el servo en cada loop
        self.speed = 5

        #Se hace la conexión con el arduino
        self.robot_serial = SerialControl()
        self.robot_serial.open_serial()

    def mover_horizontal(self, dir):
        #Servo 1
        if dir == "left":
            self.pose = self.pose - self.speed
        elif dir == "right":
            self.pose += self.speed

        #Limites del servo
        if self.pose > 90:
            self.pose = 90
        elif self.pose < 0:
            self.pose = 0

        #Se le dice al arduino la nueva posicion del servo
        self.robot_serial.write_servo(1, self.pose)

    def mover_profundidad(self, dir):
        #Servo 2
        if dir == "back":
            self.pose2 = self.pose2 - self.speed
        elif dir == "front":
            self.pose2 += self.speed
        #Limites del servo
        if self.pose2 > 150:
            self.pose2 = 150
        elif self.pose2 < 40:
            self.pose2 = 40
        #Se le dice al arduino la nueva posicion del servo
        self.robot_serial.write_servo(2, self.pose2)

    def mover_vertical(self, dir):
        # Servo 3
        if dir == "down":
            self.pose3 = self.pose3 - self.speed
        elif dir == "up":
            self.pose3 += self.speed
        #Limites del servo
        if self.pose3 > 120:
            self.pose3 = 120
        elif self.pose3 < 60:
            self.pose3 = 60
        #Se le dice al arduino la nueva posicion del servo
        self.robot_serial.write_servo(3, self.pose3)

    def mover_garra(self, dir):
        # Servo 4
        if dir == "abrir":
            self.pose4 = self.pose4 - 5
        elif dir == "cerrar":
            self.pose4 += 5
        # Limites del servo
        if self.pose4 > 90:
            self.pose4 = 90
        elif self.pose4 < 0:
            self.pose4 = 0
        # Se le dice al arduino la nueva posicion del servo
        self.robot_serial.write_servo(4, self.pose4)


def main():
    #Se crea un objeto de la clase Robot_posiciones (guarda las posiciones y recibe direcciones y mueve el robot)
    robot = Robot_posiciones()
    #Se crea un objeto de la clase PedirDirecciones (Esta esperando las direcciones que le llegan a traves de la conexión ssh y las guarda)
    receptor = PedirDirecciones()


    def loop_mover():
        #Loop que mueve al robot en la direccion actual del receptor
        while receptor.status:
            #Se escoge el servo que hay que mover(Se puede hacer más bonito)
            if receptor.direccion == "left" or receptor.direccion == "right":
                robot.mover_horizontal(receptor.direccion)
            elif receptor.direccion == "up" or receptor.direccion == "down":
                robot.mover_vertical(receptor.direccion)
            elif receptor.direccion == "front" or receptor.direccion == "back":
                robot.mover_profundidad(receptor.direccion)
            elif receptor.direccion == "abrir" or receptor.direccion == "cerrar":
                robot.mover_garra(receptor.direccion)
            time.sleep(1)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        #Inician dos threads de los loops de recepción y de actuación
        #Recibe las direcciones
        f1 = executor.submit(receptor.loop_pedir)
        #Mueve el robot
        f2 = executor.submit(loop_mover)

    #Al finalizar los loops, se cierran las conexión al arduino
    robot.robot_serial.close_serial()


if __name__ == "__main__":
    main()
