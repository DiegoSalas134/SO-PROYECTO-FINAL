import heapq  # Librería para "Colas de Prioridad" (Heap). Esencial para SJF.
from Marco import Marco

class SMV:
    def __init__(self, tamaño_memoria, tamaño_pagina):
        self.tamaño_memoria = tamaño_memoria
        self.tamaño_pagina = tamaño_pagina
        
        # División entera (//) para saber cuántos marcos caben. Ej: 32MB / 4MB = 8 Marcos.
        self.num_marcos = tamaño_memoria // tamaño_pagina
        
        # List Comprehension: Una forma rápida de crear una lista de objetos en una línea.
        # Crea 'num_marcos' objetos Marco.
        self.marcos = [Marco(i) for i in range(self.num_marcos)]
        
        # Diccionario {} para la tabla de páginas. Es como una agenda telefónica.
        # Clave: ID Proceso -> Valor: {Pagina Virtual : Marco Fisico}
        self.tabla_paginas = {}
        
        # Esta lista será nuestra cola de listos.
        self.cola_procesos = []
        self.tiempo = 0  # Reloj del sistema
        
    def agregar_proceso(self, proceso):
        # AQUI OCURRE LA MAGIA DEL SJF.
        # heapq ordena automáticamente basándose en el primer elemento de la tupla.
        # Tupla: (Prioridad 1, Prioridad 2, Objeto)
        # 1. proceso.tiempo_restante: Para que sea SJF (el más corto primero).
        # 2. proceso.tiempo_llegada: Para desempatar (el que llegó primero).
        heapq.heappush(self.cola_procesos, (proceso.tiempo_restante, proceso.tiempo_llegada, proceso))
        
    def ejecutar_sjf(self):
        # Si la lista está vacía (False), retornamos mensaje.
        if not self.cola_procesos:
            return "NO HAY NADA QUE PROCESAR"

        # .heappop() saca y elimina el elemento más pequeño (el de menor tiempo restante).
        prioridad, llegada, proceso = heapq.heappop(self.cola_procesos)
        
        out = f"--- Tiempo Sistema: {self.tiempo} ---\n"
        out += f"Intentando ejecutar {proceso.id} (Resta: {proceso.tiempo_restante})\n"

        # --- FASE 1: PAGINACIÓN (CARGAR EN MEMORIA) ---
        if not proceso.en_memoria:
            # Fórmula matemática para redondear hacia arriba la división.
            # Ej: Si tamaño es 9 y pág es 4. (9+4-1)//4 = 3 páginas.
            num_paginas = (proceso.tamaño + self.tamaño_pagina - 1) // self.tamaño_pagina
            
            # Filtramos la lista de marcos para ver cuáles no están ocupados
            marcos_libres = [m for m in self.marcos if not m.ocupado]

            # Verificamos si caben todas las páginas (Carga Atómica)
            if len(marcos_libres) >= num_paginas:
                for i in range(num_paginas):
                    marco = self.obtener_marco_libre() # Busca uno libre
                    marco.definir(proceso.id, i)       # Lo ocupa
                    
                    # Si el proceso no tiene entrada en la agenda (tabla), creamos una
                    if proceso.id not in self.tabla_paginas:
                        self.tabla_paginas[proceso.id] = {}
                    
                    # Guardamos el mapeo: Pagina i -> Marco ID
                    self.tabla_paginas[proceso.id][i] = marco.id
                    proceso.paginas.append(marco.id)
                
                proceso.en_memoria = True
                out += f"  -> Carga exitosa: {num_paginas} páginas asignadas.\n"
            else:
                # FALLO DE PAGINA: No hay RAM suficiente.
                out += "  ⚠️ FALLO DE PÁGINA: No hay suficientes marcos libres.\n"
                out += "  -> Proceso reencolado (bloqueado por memoria).\n"
                
                # Devolvemos el proceso a la cola para intentarlo luego.
                heapq.heappush(self.cola_procesos, (proceso.tiempo_restante, proceso.tiempo_llegada, proceso))
                return out # Terminamos esta ejecución aquí

        # --- FASE 2: CPU BURST (EJECUCIÓN) ---
        # Simulamos que corre por 5 segundos o menos si le falta poco.
        tiempo_ejec = min(proceso.tiempo_restante, 5)
        
        proceso.reducir_tiempo(tiempo_ejec)
        self.tiempo += tiempo_ejec
        out += f"  ⚡ Ejecutando por {tiempo_ejec}s. Restante: {proceso.tiempo_restante}s\n"

        # --- FASE 3: VERIFICACIÓN ---
        if proceso.tiempo_restante <= 0:
            out += f"  ✅ PROCESO {proceso.id} TERMINADO. Liberando memoria...\n"
            self.liberar_marcos(proceso) # Llamamos a la función de limpieza
        else:
            out += f"  🔄 Proceso {proceso.id} incompleto. Regresa a cola SJF.\n"
            # Como no terminó, vuelve a la cola. 
            # IMPORTANTE: Al volver, se reordena automáticamente según su NUEVO tiempo restante.
            heapq.heappush(self.cola_procesos, (proceso.tiempo_restante, proceso.tiempo_llegada, proceso))

        return out

    def obtener_marco_libre(self):
        # Recorre todos los marcos y devuelve el primero que no esté ocupado
        for m in self.marcos:
            if not m.ocupado:
                return m
        return None

    def liberar_marcos(self, proceso):
        # Recorre la lista de IDs de marcos que tenía el proceso
        for m_id in proceso.paginas:
            self.marcos[m_id].liberar() # Les dice a los marcos "sean libres"
            
        proceso.en_memoria = False
        proceso.paginas = []
        
        # .pop() elimina la entrada del diccionario (borra de la tabla de páginas)
        self.tabla_paginas.pop(proceso.id, None)

    def estado_memoria(self):
        # Crea una cadena de texto gigante con el estado de todos los marcos
        return "\n".join(str(m) for m in self.marcos)

    def estado_tabla_paginas(self):
        res = ""
        if not self.tabla_paginas:
            return "Tabla vacía."
        # .items() nos permite recorrer Clave y Valor al mismo tiempo
        for pid, pags in self.tabla_paginas.items():
            res += f"Proceso {pid}: {pags}\n"
        return res
    
    def obtener_cola_str(self):
        # Función visual para mostrar quién sigue en la cola
        # sorted() crea una copia ordenada de la lista sin romper el heap original
        procesos_ordenados = sorted(self.cola_procesos)
        res = "Cola SJF (Orden de ejecución):\n"
        for p in procesos_ordenados:
            proc = p[2] # El proceso es el tercer elemento de la tupla (restante, llegada, proceso)
            res += f"-> {proc.id} (Resta: {proc.tiempo_restante})\n"
        return res