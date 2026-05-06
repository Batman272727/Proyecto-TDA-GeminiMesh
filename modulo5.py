import datetime

class EventoError:
    def __init__(self, codigo, descripcion):
        self.fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.codigo = codigo
        self.descripcion = descripcion
        self.siguiente = None

class LogErrores:
    def __init__(self):
        self.cabeza = None
        self.ultimo = None

    def registrar(self, codigo, descripcion):
        nuevo = EventoError(codigo, descripcion)
        if not self.cabeza:
            self.cabeza = self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo

    def listar(self):
        print("\n=== LOG DE ERRORES ===")
        actual = self.cabeza
        if not actual:
            print("No hay errores registrados.")
        while actual:
            print(f"[{actual.fecha_hora}] Código: {actual.codigo} | {actual.descripcion}")
            actual = actual.siguiente
        print("======================")