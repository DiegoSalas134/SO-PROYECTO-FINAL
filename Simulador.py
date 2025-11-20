import heapq
from Marco import Marco
from Proceso import Proceso

class SMV:
    def __init__(self, tamaño_memoria, tamaño_pagina):
        self.tamaño_memoria = tamaño_memoria
        self.tamaño_pagina = tamaño_pagina
        self.num_marcos = tamaño_memoria // tamaño_pagina
        self.marcos = [Marco(i) for i in range(self.num_marcos)]
        self.tabla_paginas = {}
        self.cola_procesos = []
        self.tiempo = 0
        
    def agregar_proceso(self, proceso):
        heapq.heappush(self.cola_procesos, (proceso.tiempo_llegada, proceso))
        
    def ejecutar_sjf(self):
        if not self.cola_procesos:
            return "NO HAY NADA QUE PROCESAR"

        _, proceso = heapq.heappop(self.cola_procesos)
        out = f"Ejecutando {proceso} en el tiempo {self.tiempo}\n"

        num_paginas = (proceso.tamaño + self.tamaño_pagina - 1) // self.tamaño_pagina

        for i in range(num_paginas):
            marco = self.obtener_marco_libre()
            if marco:
                marco.definir(proceso.id, i)
                if proceso.id not in self.tabla_paginas:
                    self.tabla_paginas[proceso.id] = {}
                self.tabla_paginas[proceso.id][i] = marco.id
                proceso.paginas.append(marco.id)
                out += f" Página {i} asignada al Marco {marco.id}\n"
            else:
                out += " NO HAY MARCOS DISPONIBLES\n"
                heapq.heappush(self.cola_procesos, (proceso.tamaño, proceso))
                return out

        proceso.en_memoria = True
        tiempo_ejec = min(proceso.tiempo_restante, 5)
        proceso.reducir_tiempo(tiempo_ejec)
        self.tiempo += tiempo_ejec
        out += f" Ejecutado por {tiempo_ejec} unidades.\n"

        if proceso.tiempo_restante <= 0:
            out += f" PROCESO {proceso.id} COMPLETADO\n"
            self.liberar_marcos(proceso)
        else:
            out += f" Proceso {proceso.id} reinsertado\n"
            heapq.heappush(self.cola_procesos, (proceso.tamaño, proceso))

        return out

    def obtener_marco_libre(self):
        for m in self.marcos:
            if not m.ocupado:
                return m
        return None

    def liberar_marcos(self, proceso):
        for m in proceso.paginas:
            self.marcos[m].liberar()
        proceso.en_memoria = False
        self.tabla_paginas.pop(proceso.id, None)

    def estado_memoria(self):
        return "\n".join(str(m) for m in self.marcos)

    def estado_tabla_paginas(self):
        return str(self.tabla_paginas)