import tkinter as tk
from tkinter import messagebox
from Simulador import SMV
from Proceso import Proceso


class VentanaSMV:
    def __init__(self):
        self.sim = SMV(tamaño_memoria=64, tamaño_pagina=4)

        self.root = tk.Tk()
        self.root.title("Simulador SJF - Memoria Virtual")

        # Entrada de datos
        tk.Label(self.root, text="ID:").grid(row=0, column=0)
        self.e_id = tk.Entry(self.root)
        self.e_id.grid(row=0, column=1)

        tk.Label(self.root, text="Tamaño (MB):").grid(row=1, column=0)
        self.e_tam = tk.Entry(self.root)
        self.e_tam.grid(row=1, column=1)

        tk.Label(self.root, text="Tiempo llegada:").grid(row=2, column=0)
        self.e_ll = tk.Entry(self.root)
        self.e_ll.grid(row=2, column=1)

        tk.Button(self.root, text="Agregar Proceso", command=self.agregar_proceso).grid(row=3, column=0, columnspan=2)

        tk.Button(self.root, text="Ejecutar SJF", command=self.ejecutar).grid(row=4, column=0, columnspan=2)

        # Output
        self.texto = tk.Text(self.root, width=60, height=20)
        self.texto.grid(row=5, column=0, columnspan=2)

        tk.Button(self.root, text="Ver Memoria", command=self.mostrar_memoria).grid(row=6, column=0)
        tk.Button(self.root, text="Ver Tabla de Páginas", command=self.mostrar_paginas).grid(row=6, column=1)

    def agregar_proceso(self):
        try:
            pid = self.e_id.get()
            tam = int(self.e_tam.get())
            ll = int(self.e_ll.get())
        except:
            messagebox.showerror("Error", "Datos inválidos.")
            return

        proc = Proceso(pid, tam, ll)
        self.sim.agregar_proceso(proc)
        self.texto.insert(tk.END, f"Proceso {pid} agregado.\n")

    def ejecutar(self):
        out = self.sim.ejecutar_sjf()
        self.texto.insert(tk.END, out + "\n")

    def mostrar_memoria(self):
        self.texto.insert(tk.END, "\n=== MEMORIA ===\n")
        self.texto.insert(tk.END, self.sim.estado_memoria() + "\n")

    def mostrar_paginas(self):
        self.texto.insert(tk.END, "\n=== TABLA DE PÁGINAS ===\n")
        self.texto.insert(tk.END, self.sim.estado_tabla_paginas() + "\n")

    def run(self):
        self.root.mainloop()