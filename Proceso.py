class Proceso:
    def __init__(self, id, tamaño, tiempo_llegada):
        self.id=id
        self.tamaño=tamaño
        self.tiempo_llegada=tiempo_llegada
        self.tiempo_restante=tamaño
        self.tiempo_ejecucion=tamaño
        self.en_memoria=False
        self.paginas=[]
        
    def reducir_tiempo(self, tiempo):
        self.tiempo_restante -= tiempo
        
    def __str__(self):
        return f"PROCESO {self.id} (TAM: {self.tamaño}MB, TIEMPO RESTANTE: {self.tiempo_restante})"