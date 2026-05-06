from modulo1 import GestorConfiguracion
from modulo4 import GestorArchivos
from modulo5 import LogErrores
from gemini_api import chat_with_gemini


def menu_principal():
    print("""
========= GEMINIMESH CLI =========
1. Gestionar Chatbots
2. Simular Chat
3. Laboratorio de Personalidad
4. Monitor de Errores
5. Guardar Sistema
6. Cargar Sistema
0. Salir
==================================
""")

def menu_gestion():
    print("""
--- Gestión de Chatbots ---
1. Registrar nuevo bot
2. Listar bots
3. Eliminar bot
0. Volver al menú principal
""")

def menu_personalidad():
    print("""
--- Laboratorio de Personalidad ---
1. Modificar Prompt/base o modelo
2. Restaurar estado anterior
0. Volver al menú principal
""")

def input_opcion(msg, rango_validos):
    while True:
        try:
            op = int(input(msg))
            if op in rango_validos:
                return op
            print("Opción inválida. Intenta de nuevo.")
        except ValueError:
            print("Ingresa un número válido.")

def run_cli():
    gestor = GestorConfiguracion()
    log = LogErrores()
    archivos = GestorArchivos()

    while True:
        menu_principal()
        op = input_opcion("Selecciona opción: ", {0,1,2,3,4,5,6})
        if op == 1:  # Gestión
            while True:
                menu_gestion()
                opg = input_opcion("Opción: ", {0,1,2,3})
                if opg == 1:
                    idb = input("ID: ")
                    nombre = input("Nombre: ")
                    modelo = input("Modelo (ej: gemini-1.5-flash): ")
                    api_key = input("API Key: ")
                    prompt = input("System Instruction: ")
                    gestor.crear_perfil(idb, nombre, modelo, api_key, prompt, log)
                elif opg == 2:
                    gestor.listar_perfiles()
                elif opg == 3:
                    idx = input("ID a eliminar: ")
                    gestor.eliminar_perfil(idx, log)
                elif opg == 0:
                    break

        elif op == 2:  # Simulador chat simple
            gestor.listar_perfiles()
            idb = input("ID de bot para chatear: ")
            bot = gestor.consultar_perfil(idb)
            if not bot:
                log.registrar("E101", "Bot no válido para simular chat.")
                print("Bot no encontrado.")
                continue
            print("\n*Simulación de chat (escribe 'exit' para volver)*")
            while True:
                print("\n--- HISTORIAL ---")
                for msg in bot.cola_mensajes.obtener_como_lista():
                    print(f"{msg['rol']}: {msg['contenido']}")
                inp = input(f"[TU]: ")
                if inp.lower() == "exit":
                    break
                # (Simulación) El bot simplemente repite/ack. Aquí puedes poner integración real con API
                bot.cola_mensajes.encolar({"rol": "user", "contenido": inp})
                respuesta_fake = f"Echo: {inp}"
                bot.cola_mensajes.encolar({"rol": "bot", "contenido": respuesta_fake})

        elif op == 3:
            while True:
                menu_personalidad()
                opp = input_opcion("Opción: ", {0,1,2})
                if opp == 1:
                    idb = input("ID de bot: ")
                    bot = gestor.consultar_perfil(idb)
                    if not bot:
                        log.registrar("E101", "Bot no válido para modificar.")
                        print("Bot no encontrado.")
                        continue
                    nuevo_instruccion = input("Nuevo system instruction (deja vacío para no cambiar): ")
                    nuevo_modelo = input("Nuevo modelo (deja vacío para no cambiar): ")
                    gestor.modificar_perfil(
                        idb, 
                        nueva_instruccion=nuevo_instruccion if nuevo_instruccion else None,
                        nuevo_modelo=nuevo_modelo if nuevo_modelo else None,
                        log=log)
                elif opp == 2:
                    idb = input("ID de bot para restaurar estado: ")
                    bot = gestor.consultar_perfil(idb)
                    if not bot:
                        log.registrar("E101", "Bot no válido para restaurar.")
                        print("Bot no encontrado.")
                        continue
                    anterior = bot.pila_estados.desapilar()
                    if anterior:
                        bot.system_instruction = anterior.system_instruction
                        bot.modelo = anterior.modelo
                        print("Estado restaurado correctamente.")
                    else:
                        log.registrar("E105", "No hay estado previo para restaurar.")
                        print("No hay estado previo para restaurar.")
                elif opp == 0:
                    break

        elif op == 4:
            log.listar()
        elif op == 5:
            archivos.guardar_sistema(gestor)
        elif op == 6:
            archivos.cargar_sistema(gestor)
        elif op == 0:
            print("Hasta luego.")
            break

if __name__ == "__main__":
    run_cli()