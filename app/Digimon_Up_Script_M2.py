import time
from Misc_Features import iniciar_logger

from Emulator_Manager import (
    iniciar_emulador, 
    esperar_emulador_listo, 
    limpiar_anuncios_emulador,
    posicionar_emulador_a_la_izquierda,
    cerrar_emulador,
)
from Digimon_Up_Main import (
    iniciar_app, 
    anuncios, 
    recompensas,
    granja_de_carne,
    cerrar_app, 
    APLICACION
)

def main_script():
    #Emulator Manager 
    iniciar_emulador()
    time.sleep(10.0)
    
    posicionar_emulador_a_la_izquierda()

    if not esperar_emulador_listo(timeout=300.0, img_referencia_escritorio="SA.png"):
        cerrar_emulador()
        return

    limpiar_anuncios_emulador()

    #Digimon_Up_Main
    if not iniciar_app():
        print("Abortando rutina por fallo de arranque en el juego.")
        cerrar_emulador()
        return
    time.sleep(2.0)

    anuncios()
    time.sleep(2.0)

    recompensas()
    time.sleep(2.0)

    granja_de_carne()
    time.sleep(2.0)

    cerrar_app(nombre_app=APLICACION, img_borrar_todo="BT.png")

    cerrar_emulador()

if __name__ == "__main__":
    iniciar_logger(prefijo="Digimon_Up_M2")
    main_script()