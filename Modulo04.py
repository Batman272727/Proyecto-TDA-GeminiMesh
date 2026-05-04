import json
import os

class GestorArchivos:
    def __init__(self, ruta_config="configuracion.json"):
        # La ruta del archivo json debe estar guardado en un archivo de configuracion.
        self.ruta_config = ruta_config
        self.ruta_datos = self._obtener_ruta_datos()

    def _obtener_ruta_datos(self):
        """Lee el archivo de configuración para saber dónde está el JSON principal."""
        if os.path.exists(self.ruta_config):
            with open(self.ruta_config, 'r', encoding='utf-8') as archivo:
                config = json.load(archivo)
                # Si existe, retorna la ruta guardada, si no, usa una por defecto
                return config.get("ruta_json", "chatbots_db.json")
        else:
            # Si el archivo de configuración no existe, lo crea automáticamente
            config_por_defecto = {"ruta_json": "chatbots_db.json"}
            with open(self.ruta_config, 'w', encoding='utf-8') as archivo:
                json.dump(config_por_defecto, archivo, indent=4)
            return "chatbots_db.json"

    def guardar_sistema(self, lista_bots):
        """
        Guarda la red de chatbots en un archivo json.
        """
        datos_a_guardar = []
        
        # Empezamos desde el primer nodo de la Lista Enlazada Doble
        nodo_actual = lista_bots.cabeza

        while nodo_actual is not None:
            # Creamos un diccionario con los datos del bot actual
            datos_bot = {
                "id": nodo_actual.id_unico,
                "nombre": nodo_actual.nombre,
                "modelo": nodo_actual.modelo,
                "api_key": nodo_actual.api_key, 
                "system_instruction": nodo_actual.system_instruction,
                "contexto": nodo_actual.cola_mensajes.obtener_como_lista(), 
                "estados": nodo_actual.pila_estados.obtener_como_lista()
            }
            datos_a_guardar.append(datos_bot)
            
            # Pasamos al siguiente nodo
            nodo_actual = nodo_actual.siguiente

        # Escribimos toda la lista de diccionarios en el archivo JSON
        with open(self.ruta_datos, 'w', encoding='utf-8') as archivo:
            json.dump(datos_a_guardar, archivo, indent=4)
        print(f"Sistema guardado exitosamente en {self.ruta_datos}")

    def cargar_sistema(self, lista_bots):
        """
        Reconstruye todas las estructuras al iniciar el programa
        Al restaurar, se deben reconstruir los punteros de las listas, las colas de mensajes y las pilas de estados en el orden correcto.
        """
        if not os.path.exists(self.ruta_datos):
            print("No hay datos guardados previos. Iniciando sistema en blanco.")
            return

        with open(self.ruta_datos, 'r', encoding='utf-8') as archivo:
            datos_cargados = json.load(archivo)

        # Recorremos el JSON y vamos reconstruyendo la memoria dinámica
        for datos_bot in datos_cargados:
            
            # 1. Reconstruir el Nodo y los punteros de la Lista (Módulo 1)
            nodo_nuevo = lista_bots.insertar_bot(
                datos_bot["id"],
                datos_bot["nombre"],
                datos_bot["modelo"],
                datos_bot["api_key"],
                datos_bot["system_instruction"]
            )

            # 2. Reconstruir la Cola de Contexto (Módulo 2)
            for mensaje in datos_bot["contexto"]:
                # Asumiendo que tu método se llama 'encolar'
                nodo_nuevo.cola_mensajes.encolar(mensaje)

            # 3. Reconstruir la Pila de Restauración (Módulo 3)
            for estado in datos_bot["estados"]:
                # Asumiendo que tu método se llama 'apilar' o 'push'
                nodo_nuevo.pila_estados.apilar(estado)
                
        print("Estructuras y punteros reconstruidos correctamente.")