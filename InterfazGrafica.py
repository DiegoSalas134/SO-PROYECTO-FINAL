import tkinter as tk            # Librería para crear ventanas (GUI)
from tkinter import messagebox  # Librería para mostrar alertas (pop-ups)
import time                     # Librería para controlar el tiempo (pausas)
from Simulador import SMV       # Importamos el cerebro (Lógica)
from Proceso import Proceso     # Importamos la estructura de datos (Procesos)

class VentanaSMV:
    def __init__(self):
        self.sim = None       # Variable vacía donde guardaremos el simulador más tarde
        self.root = tk.Tk()   # Creamos la ventana principal (Raíz)
        self.root.title("Simulador SJF - Proyecto Final SO") # Título de la ventana
        self.root.geometry("650x700") # Tamaño: Ancho x Alto

        # Frame principal: Es un contenedor invisible para organizar todo adentro
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True) # .pack lo "pega" a la ventana

        # Llamamos a la primera pantalla: La configuración
        self.mostrar_configuracion()

    def mostrar_configuracion(self):
        # Limpieza: Borramos cualquier cosa que haya antes en la ventana
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Título
        tk.Label(self.main_frame, text="CONFIGURACIÓN INICIAL", font=("Arial", 14, "bold")).pack(pady=10)

        # Campo para Memoria Total
        tk.Label(self.main_frame, text="Tamaño Total Memoria (MB):").pack()
        self.e_mem = tk.Entry(self.main_frame) # Cajita blanca para escribir
        self.e_mem.insert(0, "64") # Escribimos "64" por defecto para ayudar al usuario
        self.e_mem.pack()

        # Campo para Tamaño de Página
        tk.Label(self.main_frame, text="Tamaño de Página (MB):").pack()
        self.e_pag = tk.Entry(self.main_frame)
        self.e_pag.insert(0, "4") # "4" por defecto
        self.e_pag.pack()

        # Botón para guardar y avanzar
        tk.Button(self.main_frame, text="Iniciar Simulador", command=self.crear_simulador, bg="#DDDDDD").pack(pady=20)

    def crear_simulador(self):
        try:
            # Obtenemos el texto de las cajitas (.get) y lo convertimos a número (int)
            mem = int(self.e_mem.get())
            pag = int(self.e_pag.get())
            
            # Validación lógica: La página no puede ser más grande que toda la RAM
            if pag > mem:
                messagebox.showerror("Error", "La página no puede ser mayor a la memoria.")
                return
            
            # ¡Aquí nace el simulador! Creamos el objeto SMV con los datos
            self.sim = SMV(mem, pag)
            
            # Cambiamos de pantalla a la de simulación
            self.mostrar_simulacion()
        except ValueError:
            # Si escriben letras en vez de números, mostramos error
            messagebox.showerror("Error", "Por favor ingrese números enteros válidos.")

    def mostrar_simulacion(self):
        # Limpieza de pantalla otra vez
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # --- SECCIÓN 1: AGREGAR PROCESOS ---
        # LabelFrame pone un marco con título alrededor
        frame_input = tk.LabelFrame(self.main_frame, text="Nuevo Proceso")
        frame_input.pack(fill="x", pady=5) # fill="x" estira el marco a lo ancho

        # Usamos .grid (filas y columnas) para ordenar bonito los inputs
        tk.Label(frame_input, text="ID:").grid(row=0, column=0)
        self.e_id = tk.Entry(frame_input, width=10)
        self.e_id.grid(row=0, column=1)

        tk.Label(frame_input, text="Tamaño (MB):").grid(row=0, column=2)
        self.e_tam = tk.Entry(frame_input, width=10)
        self.e_tam.grid(row=0, column=3)
        
        tk.Label(frame_input, text="Llegada:").grid(row=0, column=4)
        self.e_ll = tk.Entry(frame_input, width=10)
        self.e_ll.grid(row=0, column=5)

        # Botón verde claro (#CCFFCC) para agregar a la cola
        tk.Button(frame_input, text="Agregar", command=self.agregar_proceso, bg="#CCFFCC").grid(row=0, column=6, padx=10)

        # --- SECCIÓN 2: BOTONES DE CONTROL ---
        frame_ctrl = tk.Frame(self.main_frame)
        frame_ctrl.pack(pady=5)
        
        # Botón Manual (Naranja): Ejecuta solo un paso
        tk.Button(frame_ctrl, text="PASO A PASO", command=self.ejecutar, bg="#FFCC99", height=2).pack(side=tk.LEFT, padx=5)
        
        # Botón Automático (Verde Fuerte): Ejecuta todo el bucle <--- NUEVO
        tk.Button(frame_ctrl, text="EJECUTAR TODO (AUTO)", command=self.ejecutar_todo, bg="#99FF99", height=2).pack(side=tk.LEFT, padx=5)

        # Botones informativos (Ver memoria y tablas)
        tk.Button(frame_ctrl, text="Ver Memoria Física", command=self.ver_memoria).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_ctrl, text="Ver Tabla Páginas", command=self.ver_paginas).pack(side=tk.LEFT, padx=5)

        # --- SECCIÓN 3: PANELES VISUALES (COLA Y LOG) ---
        # PanedWindow divide la pantalla en dos áreas ajustables
        paned = tk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=5)

        # IZQUIERDA: Visualizador de la Cola SJF
        frame_cola = tk.LabelFrame(paned, text="Cola de Listos (SJF)")
        # Label grande donde pondremos el texto de quién sigue
        self.lbl_cola = tk.Label(frame_cola, text="Vacía", justify=tk.LEFT, anchor="nw", bg="white", relief="sunken")
        self.lbl_cola.pack(fill=tk.BOTH, expand=True)
        paned.add(frame_cola, width=200)

        # DERECHA: Bitácora o Log (Texto scrolleable)
        frame_log = tk.LabelFrame(paned, text="Bitácora de Ejecución")
        self.txt_log = tk.Text(frame_log, width=40, height=15)
        self.txt_log.pack(fill=tk.BOTH, expand=True)
        paned.add(frame_log)

    def agregar_proceso(self):
        try:
            # Recolectamos datos
            pid = self.e_id.get()
            tam = int(self.e_tam.get())
            ll = int(self.e_ll.get())
            if not pid: raise ValueError # Error si el ID está vacío
            
            # Creamos el objeto Proceso y lo enviamos al Simulador
            p = Proceso(pid, tam, ll)
            self.sim.agregar_proceso(p)
            
            # Avisamos en el log
            self.txt_log.insert(tk.END, f"Proceso {pid} agregado a la cola.\n")
            self.actualizar_cola_visual() # Refrescamos la lista de la izquierda
            
            # Limpiamos las cajitas para el siguiente
            self.e_id.delete(0, tk.END)
            self.e_tam.delete(0, tk.END)
            self.e_ll.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Datos inválidos. Revise ID, Tamaño y Llegada.")

    # --- FUNCIÓN 1: EJECUCIÓN MANUAL ---
    def ejecutar(self):
        # Verificamos si hay alguien en la cola
        if not self.sim.cola_procesos:
            messagebox.showinfo("Info", "No hay procesos pendientes.")
            return

        # Llamamos al cerebro para que haga UN solo cálculo
        resultado = self.sim.ejecutar_sjf()
        
        # Escribimos el resultado en pantalla
        self.txt_log.insert(tk.END, resultado + "\n")
        self.txt_log.see(tk.END) # Scroll automático hacia abajo
        self.actualizar_cola_visual()

    # --- FUNCIÓN 2: EJECUCIÓN AUTOMÁTICA (NUEVA) ---
    def ejecutar_todo(self):
        # Validación inicial
        if not self.sim.cola_procesos:
            messagebox.showinfo("Info", "No hay procesos para ejecutar.")
            return

        # BUCLE WHILE: "Mientras la cola NO esté vacía, sigue repitiendo"
        while self.sim.cola_procesos:
            
            # 1. Hacemos el cálculo (igual que en el manual)
            resultado = self.sim.ejecutar_sjf()
            
            # 2. Imprimimos el resultado
            self.txt_log.insert(tk.END, resultado + "\n")
            self.txt_log.see(tk.END)
            self.actualizar_cola_visual()
            
            # 3. TRUCO VISUAL: .update() fuerza a la ventana a redibujarse AHORA MISMO.
            # Sin esto, la ventana se congelaría y solo verías el final de golpe.
            self.root.update() 
            
            # 4. PAUSA DE CINE: Esperamos 0.5 segundos antes de la siguiente vuelta.
            # Esto crea el efecto de animación para que el profesor vea qué pasa.
            time.sleep(0.5) 
            
        # Cuando el while termina (la cola se vacía), ponemos mensaje final
        self.txt_log.insert(tk.END, "--- SIMULACIÓN FINALIZADA ---\n")
        self.txt_log.see(tk.END)

    def ver_memoria(self):
        # Muestra el estado de los marcos en el área de texto
        self.txt_log.insert(tk.END, "\n=== ESTADO MEMORIA FÍSICA ===\n")
        self.txt_log.insert(tk.END, self.sim.estado_memoria() + "\n")
        self.txt_log.see(tk.END)

    def ver_paginas(self):
        # Muestra el diccionario de páginas en el área de texto
        self.txt_log.insert(tk.END, "\n=== TABLA DE PÁGINAS ===\n")
        self.txt_log.insert(tk.END, self.sim.estado_tabla_paginas() + "\n")
        self.txt_log.see(tk.END)

    def actualizar_cola_visual(self):
        # Pide al simulador la lista de texto y la pone en el panel izquierdo
        texto = self.sim.obtener_cola_str()
        self.lbl_cola.config(text=texto)

    def run(self):
        # Mantiene el programa encendido esperando clicks
        self.root.mainloop()