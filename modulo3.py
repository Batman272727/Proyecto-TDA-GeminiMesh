class EstadoBot:
    def __init__(self, instruction, modelo):
        self.system_instruction = instruction
        self.modelo = modelo
        self.siguiente = None

class PilaEstados:
    def __init__(self):
        self.cima = None

    def apilar(self, instruction, modelo):
        """Guarda el estado previo."""
        nuevo = EstadoBot(instruction, modelo)
        nuevo.siguiente = self.cima
        self.cima = nuevo

    def desapilar(self):
        """Deshace (restaura) el último estado."""
        if not self.cima: 
            return None
        extraido = self.cima
        self.cima = self.cima.siguiente
        return extraido

    def obtener_como_lista(self):
        """Exporta los estados para serialización."""
        lista = []
        actual = self.cima
        while actual:
            lista.append({
                "system_instruction": actual.system_instruction,
                "modelo": actual.modelo
            })
            actual = actual.siguiente
        return lista[::-1]   # Para mantenerlo cronológico al cargar