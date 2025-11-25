class Marco:
    # __init__ es el CONSTRUCTOR. Se ejecuta automáticamente al crear un nuevo Marco.
    # 'self' se refiere al objeto mismo (este marco específico).
    def __init__(self, id):
        self.id = id              # Guardamos el número de identificación del marco (ej. Marco 0, Marco 1)
        self.ocupado = False      # Bandera (booleano): ¿Está lleno? Al principio es Falso.
        self.proceso_id = None    # ¿Qué proceso lo está usando? (None = Nadie)
        self.pagina_id = None     # ¿Qué página de ese proceso está aquí?

    # Método para "llenar" el cajón con datos
    def definir(self, proceso_id, pagina_id):
        self.ocupado = True             # Marcamos que ya no está disponible
        self.proceso_id = proceso_id    # Guardamos el dueño
        self.pagina_id = pagina_id      # Guardamos qué pedazo del dueño es
        
    # Método para vaciar el cajón (cuando el proceso termina o se va)
    def liberar(self):
        self.ocupado = False      # Lo marcamos como libre de nuevo
        self.proceso_id = None    # Borramos el dueño
        self.pagina_id = None     # Borramos la página
        
    # __str__ convierte el objeto a texto. Útil para imprimirlo en pantalla.
    # Usamos f-strings (f"texto {variable}") para insertar variables dentro del texto.
    def __str__(self):
        # Operador ternario: "Texto A" si es verdad, si no "Texto B"
        estado = f"OCUPADO (Proc {self.proceso_id} - Pág {self.pagina_id})" if self.ocupado else "LIBRE"
        return f"MARCO {self.id}: {estado}"