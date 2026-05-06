import datetime

class Mensaje:
    def __init__(self, contenido, rol):
        self.contenido = contenido
        self.rol = rol
        self.timestamp = datetime.datetime.now()
        self.siguiente = None

class ColaMensajes:
    """Cola con límite (FIFO) para el contexto."""
    def __init__(self, limite=10):
        self.frente = None
        self.final = None
        self.tamano_actual = 0
        self.limite = limite

    def encolar(self, datos_mensaje):
        """Inserta un mensaje y maneja el desbordamiento."""
        if self.tamano_actual >= self.limite:
            self.desencolar()
        if isinstance(datos_mensaje, dict):
            contenido = datos_mensaje.get('contenido')
            rol = datos_mensaje.get('rol', 'user')
        else:
            contenido = datos_mensaje
            rol = 'user'
        nuevo = Mensaje(contenido, rol)
        if not self.frente:
            self.frente = self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self.tamano_actual += 1

    def desencolar(self):
        if not self.frente:
            return None
        temp = self.frente
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        self.tamano_actual -= 1
        return temp

    def obtener_como_lista(self):
        lista = []
        actual = self.frente
        while actual:
            lista.append({"rol": actual.rol, "contenido": actual.contenido})
            actual = actual.siguiente
        return lista