class Marco:
    def __init__(self, id):
        self.id=id
        self.ocupado=False
        self.proceso_id=None
        self.pagina_id=None

    def definir(self, proceso_id,pagina_id):
        self.ocupado=True
        self.proceso_id=proceso_id
        self.pagina_id=pagina_id
        
    def liberar(self):
        self.ocupado=False
        self.proceso_id=None
        self.pagina_id=None
        
    def __str__(self):
        return f"MARCO {self.id}: {'OCUPADO' if self.ocupado else 'LIBRE'}"