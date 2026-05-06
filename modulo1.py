class PerfilGemini:
    """Representa un nodo de la Lista Enlazada Doble (Perfil de IA)"""
    
    def __init__(self, id_unico, nombre, modelo, api_key, system_instruction):
        # Datos del perfil
        self.id_unico = id_unico
        self.nombre_bot = nombre
        self.modelo = modelo # Ej: gemini-1.5-flash
        self.api_key = api_key # Debería estar encriptada
        self.system_instruction = system_instruction
        
        # Punteros a Estructuras Hijas
        self.frente_cola = None  # Referencia al Módulo 2 
        self.raiz_pila = None    # Referencia al Módulo 3 
        
        # Punteros de la Lista Doble
        self.siguiente = None
        self.anterior = None

class GestorConfiguracion:
    """TDA para gestionar la colección dinámica de perfiles[cite: 1]"""
    
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def crear_perfil(self, id_unico, nombre, modelo, api_key, instruction):
        """Crea e inserta un nuevo bot al final de la lista[cite: 1]"""
        nuevo_bot = PerfilGemini(id_unico, nombre, modelo, api_key, instruction)
        
        if not self.cabeza:
            self.cabeza = nuevo_bot
            self.cola = nuevo_bot
        else:
            nuevo_bot.anterior = self.cola
            self.cola.siguiente = nuevo_bot
            self.cola = nuevo_bot
        print(f"Bot '{nombre}' registrado correctamente.")

    def listar_perfiles(self):
        """Recorre la lista doble y muestra los bots registrados[cite: 1]"""
        actual = self.cabeza
        print("\n--- LISTADO DE PERFILES GEMINI MESH ---")
        if not actual:
            print("No hay bots configurados.")
            return
            
        while actual:
            print(f"ID: {actual.id_unico} | Nombre: {actual.nombre_bot} | Modelo: {actual.modelo}")
            actual = actual.siguiente

    def consultar_perfil(self, id_buscado):
        """Busca un perfil específico por su ID único[cite: 1]"""
        actual = self.cabeza
        while actual:
            if actual.id_unico == id_buscado:
                return actual
            actual = actual.siguiente
        return None

    def modificar_perfil(self, id_buscado, nuevo_nombre=None, nueva_instruccion=None):
        """Busca un bot y actualiza sus campos[cite: 1]"""
        bot = self.consultar_perfil(id_buscado)
        if bot:
            # Aquí se llamaría al Módulo 3 para guardar el estado anterior en la Pila antes de cambiar
            if nuevo_nombre: bot.nombre_bot = nuevo_nombre
            if nueva_instruccion: bot.system_instruction = nueva_instruccion
            print(f"Perfil {id_buscado} actualizado.")
        else:
            print(f"Error: No se encontró el bot con ID {id_buscado}.")

    def eliminar_perfil(self, id_buscado):
        """Elimina un nodo ajustando los punteros anterior y siguiente[cite: 1]"""
        bot = self.consultar_perfil(id_buscado)
        if not bot:
            print("ID no encontrado.")
            return

        # Ajuste de punteros[cite: 1]
        if bot.anterior:
            bot.anterior.siguiente = bot.siguiente
        else:
            self.cabeza = bot.siguiente

        if bot.siguiente:
            bot.siguiente.anterior = bot.anterior
        else:
            self.cola = bot.anterior
            
        # En Python, el recolector de basura libera la memoria si no hay más referencias
        print(f"Bot {id_buscado} eliminado del sistema.")       