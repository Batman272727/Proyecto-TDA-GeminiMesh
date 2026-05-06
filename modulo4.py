import json
import os

class GestorArchivos:
    def __init__(self, ruta_config="configuracion.json"):
        self.ruta_config = ruta_config
        self.ruta_datos = self._obtener_ruta_datos()

    def _obtener_ruta_datos(self):
        if os.path.exists(self.ruta_config):
            with open(self.ruta_config, 'r', encoding='utf-8') as archivo:
                config = json.load(archivo)
                return config.get("ruta_json", "chatbots_db.json")
        else:
            config_por_defecto = {"ruta_json": "chatbots_db.json"}
            with open(self.ruta_config, 'w', encoding='utf-8') as archivo:
                json.dump(config_por_defecto, archivo, indent=4)
            return "chatbots_db.json"

    def guardar_sistema(self, lista_bots):
        datos_a_guardar = []
        nodo_actual = lista_bots.cabeza
        while nodo_actual is not None:
            datos_bot = {
                "id": nodo_actual.id_unico,
                "nombre": nodo_actual.nombre_bot,
                "modelo": nodo_actual.modelo,
                "api_key": nodo_actual.api_key,
                "system_instruction": nodo_actual.system_instruction,
                "contexto": nodo_actual.cola_mensajes.obtener_como_lista(),
                "estados": nodo_actual.pila_estados.obtener_como_lista()
            }
            datos_a_guardar.append(datos_bot)
            nodo_actual = nodo_actual.siguiente
        with open(self.ruta_datos, 'w', encoding='utf-8') as archivo:
            json.dump(datos_a_guardar, archivo, indent=4)
        print(f"Sistema guardado exitosamente en {self.ruta_datos}")

    def cargar_sistema(self, lista_bots):
        if not os.path.exists(self.ruta_datos):
            print("No hay datos guardados previos. Iniciando sistema en blanco.")
            return
        # Importa aquí para evitar circularidad
        from modulo1 import PerfilGemini
        with open(self.ruta_datos, 'r', encoding='utf-8') as archivo:
            datos_cargados = json.load(archivo)
        for datos_bot in datos_cargados:
            if lista_bots.consultar_perfil(datos_bot["id"]):
                continue
            nodo_nuevo = PerfilGemini(
                datos_bot["id"],
                datos_bot["nombre"],
                datos_bot["modelo"],
                datos_bot["api_key"],
                datos_bot["system_instruction"]
            )
            # Añadir al final de la lista manualmente
            if not lista_bots.cabeza:
                lista_bots.cabeza = lista_bots.cola = nodo_nuevo
            else:
                nodo_nuevo.anterior = lista_bots.cola
                lista_bots.cola.siguiente = nodo_nuevo
                lista_bots.cola = nodo_nuevo
            # Cola de mensajes
            for mensaje in datos_bot.get("contexto", []):
                nodo_nuevo.cola_mensajes.encolar(mensaje)
            # Pila de estados
            for estado in datos_bot.get("estados", []):
                nodo_nuevo.pila_estados.apilar(
                    estado.get("system_instruction", ""),
                    estado.get("modelo", "")
                )
        print("Estructuras y punteros reconstruidos correctamente.")