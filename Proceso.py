class Proceso:
    def __init__(self, id, tamaño, tiempo_llegada):
        self.id = id
        self.tamaño = tamaño
        self.tiempo_llegada = tiempo_llegada
        
        # En SJF Expropiativo, nos importa cuánto le FALTA, no cuánto duraba al inicio.
        # Al principio, el tiempo restante es igual al tamaño total.
        self.tiempo_restante = tamaño 
        
        self.en_memoria = False  # Bandera: ¿Ya cargamos sus páginas en RAM?
        self.paginas = []        # Lista para guardar en qué marcos quedó guardado
        
    # Método para restar tiempo cuando el CPU lo ejecuta
    def reducir_tiempo(self, tiempo):
        self.tiempo_restante -= tiempo # Es igual a: self.tiempo_restante = self.tiempo_restante - tiempo
        
    # IMPORTANTE: __lt__ significa "Less Than" (Menor Que).
    # Esto le enseña a Python cómo ordenar dos procesos.
    # Necesario para que la cola de prioridad (Heap) sepa a quién poner primero.
    def __lt__(self, other):
        # Comparamos por ID para desempatar si tienen el mismo tiempo.
        # (La comparación principal de tiempo se hace en el Simulador, aquí solo desempatamos).
        return self.id < other.id

    def __str__(self):
        return f"PROCESO {self.id} (TAM: {self.tamaño} | RESTANTE: {self.tiempo_restante})"