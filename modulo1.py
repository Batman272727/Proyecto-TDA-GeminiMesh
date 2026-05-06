from modulo2 import ColaMensajes
from modulo3 import PilaEstados

class PerfilGemini:
    """Nodo del TDA. Representa el Perfil del Bot Gemini."""
    def __init__(self, id_unico, nombre, modelo, api_key, system_instruction):
        self.id_unico = id_unico
        self.nombre_bot = nombre
        self.modelo = modelo
        self.api_key = api_key  # Debería estar encriptada
        self.system_instruction = system_instruction
        # Punteros a módulos hijos
        self.cola_mensajes = ColaMensajes()
        self.pila_estados = PilaEstados()
        # Punteros doblemente enlazados
        self.siguiente = None
        self.anterior = None

class GestorConfiguracion:
    """TDA para lista doblemente enlazada de Perfiles Gemini."""
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def crear_perfil(self, id_unico, nombre, modelo, api_key, instruction, log):
        """Crea e inserta un nuevo bot al final de la lista."""
        if self.consultar_perfil(id_unico):
            log.registrar("E103", f"ID '{id_unico}' ya existe.")
            print(f"Error: El ID '{id_unico}' ya existe.")
            return
        nuevo_bot = PerfilGemini(id_unico, nombre, modelo, api_key, instruction)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo_bot
        else:
            nuevo_bot.anterior = self.cola
            self.cola.siguiente = nuevo_bot
            self.cola = nuevo_bot
        print(f"Bot '{nombre}' registrado correctamente.")

    def listar_perfiles(self):
        """Imprime todos los bots registrados."""
        actual = self.cabeza
        print("\n--- LISTADO DE PERFILES GEMINI MESH ---")
        if not actual:
            print("No hay bots configurados.")
            return
        while actual:
            print(f"ID: {actual.id_unico} | Nombre: {actual.nombre_bot} | Modelo: {actual.modelo}")
            actual = actual.siguiente

    def consultar_perfil(self, id_buscado):
        """Devuelve el perfil/bot buscado por ID."""
        actual = self.cabeza
        while actual:
            if actual.id_unico == id_buscado:
                return actual
            actual = actual.siguiente
        return None

    def modificar_perfil(self, id_buscado, nuevo_nombre=None, nueva_instruccion=None, nuevo_modelo=None, log=None):
        """Actualiza campos de un perfil y guarda el estado anterior en la pila."""
        bot = self.consultar_perfil(id_buscado)
        if bot:
            # Antes de modificar, apila el estado actual
            bot.pila_estados.apilar(bot.system_instruction, bot.modelo)
            if nuevo_nombre: bot.nombre_bot = nuevo_nombre
            if nueva_instruccion: bot.system_instruction = nueva_instruccion
            if nuevo_modelo: bot.modelo = nuevo_modelo
            print(f"Perfil '{id_buscado}' actualizado.")
        else:
            if log:
                log.registrar("E101", f"Bot con ID '{id_buscado}' no encontrado en modificación.")
            print(f"Error: No se encontró el bot con ID '{id_buscado}'.")

    def eliminar_perfil(self, id_buscado, log):
        """Elimina un bot por ID."""
        bot = self.consultar_perfil(id_buscado)
        if not bot:
            log.registrar("E101", f"ID '{id_buscado}' no encontrado para eliminar.")
            print("ID no encontrado.")
            return False

        if bot.anterior:
            bot.anterior.siguiente = bot.siguiente
        else:
            self.cabeza = bot.siguiente
        if bot.siguiente:
            bot.siguiente.anterior = bot.anterior
        else:
            self.cola = bot.anterior
        print(f"Bot '{id_buscado}' eliminado del sistema.")
        return True