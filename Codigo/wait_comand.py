class PedirDirecciones:
    def __init__(self):
        self.direccion = "stop"
        self.status = True


    def loop_pedir(self):
        #espera a que le llegue una dirección
        while True:
            self.direccion = input("Ingresa direccion: ")
            if self.direccion == "leave":
                self.status = False
                break
