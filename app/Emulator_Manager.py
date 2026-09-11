import subprocess
import time
import pygetwindow as gw
import pyautogui
from Core_Windows import obtener_rect_emulador, capturar_pantalla, buscar_coordenadas

# Ruta predeterminada del ejecutable CLI de LDPlayer
LDCONSOLE_PATH = r"F:\LDPlayer\LDPlayer14\ldconsole.exe"
TITULO_EMULADOR = "Boring Phone 14"

def iniciar_emulador(nombre_instancia=TITULO_EMULADOR):
    print(f"Iniciando instancia '{nombre_instancia}'...")
    try:
        subprocess.run([LDCONSOLE_PATH, "launch", "--name", nombre_instancia], check=True)
        return True
    except Exception as e:
        print(f"ERROR al lanzar el emulador: {e}")
        return False

def esperar_emulador_listo(timeout=300.0, img_referencia="SA.png"):

    inicio = time.time()
    print("Esperando a que la ventana del emulador responda...")
    
    ventana_encontrada = False
    while time.time() - inicio < timeout:
        rect = obtener_rect_emulador(TITULO_EMULADOR)
        if rect:
            posicionar_emulador_a_la_izquierda()
            ventana_encontrada = True
            break
        time.sleep(1.0)
        
    if not ventana_encontrada:
        print("ERROR: La ventana de LDPlayer no apareció.")
        return False
    
    rect = obtener_rect_emulador(TITULO_EMULADOR)
    pyautogui.click(rect["left"] + 200, rect["top"] + 10)
    time.sleep(1.0)

    ultimo_esc = time.time()
    
    while time.time() - inicio < timeout:
        pantalla = capturar_pantalla()
        if pantalla is not None:

            if buscar_coordenadas(img_referencia, pantalla=pantalla) or buscar_coordenadas("SA.png", pantalla=pantalla):
                print("Escritorio de Android listo y visible.")
                time.sleep(1.0)
                return True

        if time.time() - ultimo_esc >= 4.0:
            pyautogui.click(rect["left"] + 200, rect["top"] + 10)  # Re-enfocar
            pyautogui.press('esc')
            ultimo_esc = time.time()

        time.sleep(1.5)

    print("ERROR: Tiempo agotado esperando la carga de Android.")
    return False

def posicionar_emulador_a_la_derecha(titulo=TITULO_EMULADOR):
    """Mueve la ventana del emulador al borde derecho de la pantalla principal."""
    ventanas = gw.getWindowsWithTitle(titulo)
    if not ventanas:
        return False
    
    v = ventanas[0]
    if v.isMinimized:
        v.restore()
        
    ancho_pantalla, _ = pyautogui.size()
    
    nueva_x = ancho_pantalla - v.width
    nueva_y = 0 

    v.moveTo(nueva_x, nueva_y)
    print(f"Ventana '{titulo}' posicionada al borde derecho ({nueva_x}, {nueva_y}).")
    return True

import pygetwindow as gw

def posicionar_emulador_a_la_izquierda(titulo=TITULO_EMULADOR):
    """Mueve la ventana del emulador al borde superior izquierdo (0, 0)."""
    ventanas = gw.getWindowsWithTitle(titulo)
    if not ventanas:
        print(f"No se encontró la ventana '{titulo}'.")
        return False
    
    v = ventanas[0]
    if v.isMinimized:
        v.restore()
        
    # Anclar a la esquina superior izquierda
    v.moveTo(0, 0)
    print(f"Ventana '{titulo}' posicionada al borde izquierdo (0, 0).")
    return True

def cerrar_emulador(nombre_instancia=TITULO_EMULADOR):
    """Cierra la instancia de LDPlayer por completo liberando recursos."""
    print(f"Cerrando instancia '{nombre_instancia}'...")
    try:
        subprocess.run([LDCONSOLE_PATH, "quit", "--name", nombre_instancia], check=True)
        return True
    except Exception as e:
        print(f"ERROR al cerrar el emulador: {e}")
        return False

if __name__ == "__main__":
    iniciar_emulador()
    if esperar_emulador_listo():
        posicionar_emulador_a_la_derecha() # <-- Mueve la ventana al borde derecho
        time.sleep(60)
        cerrar_emulador()