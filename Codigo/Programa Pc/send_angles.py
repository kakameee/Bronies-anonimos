import numpy as np
import time
import paramiko


#ngrok puerto 17056, ip 0.tcp.sa.ngrok.io
#fablab puerto 22, ip 192.168.0.14


def rad_to_grad(angulo):
    grados = (angulo * 180 / np.pi)
    return grados


class ConectarRaspy:

    def __init__(self, HOST="192.168.0.11", USER="pi", password="qwe123qwe"):

        #Se conecta a la raspi via ssh
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(HOST, username=USER, password=password, port=22)

        #se invoca una shell de la raspi en el programa
        self.channel = self.client.invoke_shell()
        #se inicia el programa de la raspi encargado de mover el robot y recibir la información
        self.entrar_al_programa()


    def wait_recv_ready(self):
        #Espera a que la raspi pueda recibir comandos
        #si se demora mucho se rinde (mas de 50 seg)
        c = time.time()
        while True:
            if self.channel.recv_ready():
                break

            elif time.time() - c > 50:
                print("conexion falllida")
                break



    def entrar_al_programa(self):
        #entra al programa de la raspi
        self.wait_recv_ready()

        """Se realizan los siguientes pasos:
            1. activar el entorno virtual
            2. iniciar el programa 
        """
        if self.channel.recv_ready():
            print(self.channel.recv(9999).decode())
            cmd = "workon mlf"
            cmd += "\n"
            self.channel.send(cmd.encode())
            print("Entorno Virtual Listo")
        else:
            print("no se pudo conectar al entorno virtual")
            return
        self.wait_recv_ready()
        if self.channel.recv_ready():
            print(self.channel.recv(9999).decode())
            cmd = "python mlf/core/mover_en_raspi.py"
            cmd += "\n"
            self.channel.send(cmd.encode())
            print("Programa Iniciado")
            return
        else:
            print("no se pudo iniciar el programa")

    def mandar_direccion(self, direccion):
        #Manda la dirección a la raspi
        self.wait_recv_ready()
        if self.channel.recv_ready():
            direccion += "\n"
            self.channel.send(direccion.encode())
            print("direccion: " + direccion)
        else:
            print("No se pudo mandar la dirección")
            return

    def close(self):
        self.client.close()


"""CODIGO PARA PRUEBAS DE LA CONSOLA"""

if __name__ == "__main__":
    HOST = "0.tcp.sa.ngrok.io"
    USER = "pi"
    password = "qwe123qwe"

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=password, port=17056)

        channel = client.invoke_shell()
        channel_data = ""
        host = ""
        srcfile = ""

        c = 0

        while True:
            if channel.recv_ready():
                channel_data += channel.recv(9999).decode()
                print("##### Device Output ######")
                print(channel_data)
                print("########################")
                c = 0
            elif (c == 5):
                break
            else:
                c += 1
                time.sleep(1)
                continue
            cmd = input("$>")
            if cmd == "exit": break
            cmd += "\n"
            channel.send(cmd.encode())

        client.close()


    except paramiko.ssh_exception.AuthenticationException as e:
        print("Autentificación fallida.")
