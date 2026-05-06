from datetime import datetime

class NodoError:
    "Nodo individual que representa un evento de error"
    def __init__(self, codigo_error, descripcion):
        # Captura la fecha y hora actual automáticamente
        self.fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.codigo_error = codigo_error
        self.descripcion = descripcion
        self.siguiente = None  # Puntero al siguiente error en la lista

class ListaErrores:
    """Lista Enlazada de eventos cronológicos para la auditoría del sistema"""
    def __init__(self):
        self.cabeza = None
        # Mantenemos un puntero a la cola para que insertar errores sea instantáneo
        self.cola_nodo = None 

    def registrar_error(self, codigo_error, descripcion):
        """Crea un nuevo nodo de error y lo añade al final de la lista."""
        nuevo_error = NodoError(codigo_error, descripcion)

        if self.cabeza is None:
            # Si la lista está vacía, el primer error es la cabeza y la cola
            self.cabeza = nuevo_error
            self.cola_nodo = nuevo_error
        else:
            # Si ya hay errores, conectamos el nuevo al final y actualizamos la cola
            self.cola_nodo.siguiente = nuevo_error
            self.cola_nodo = nuevo_error
            
        # Opcional: Imprime en consola para que veas que funciona mientras programas
        print(f"[LOG DE SISTEMA] {nuevo_error.fecha_hora} - Error {codigo_error}: {descripcion}")

    def mostrar_log_consola(self):
        """Recorre la lista y muestra los errores (Ideal si estuvieras haciendo la Opción A)."""
        if self.cabeza is None:
            print("El sistema no ha registrado errores.")
            return

        print("\n--- HISTORIAL DE INCIDENCIAS ---")
        actual = self.cabeza
        while actual is not None:
            print(f"[{actual.fecha_hora}] {actual.codigo_error}: {actual.descripcion}")
            actual = actual.siguiente
        print("--------------------------------\n")

    def obtener_errores_gui(self):
        """
        Extrae los errores en una lista normal de diccionarios.
        Esto es perfecto para la Opción B (Interfaz Gráfica) para mostrarlo en un panel visual[cite: 1].
        """
        lista_errores = []
        actual = self.cabeza
        while actual is not None:
            lista_errores.append({
                "fecha_hora": actual.fecha_hora,
                "codigo": actual.codigo_error,
                "descripcion": actual.descripcion
            })
            actual = actual.siguiente
        return lista_errores