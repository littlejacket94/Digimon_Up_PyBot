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

def esperar_emulador_listo(timeout=300.0, img_referencia_escritorio="SA.png"):

    inicio = time.time()
    print("Esperando a que la ventana del emulador responda...")
    
    # 1. Esperar registro de la ventana
    while time.time() - inicio < timeout:
        rect = obtener_rect_emulador(TITULO_EMULADOR)
        if rect:
            break
        time.sleep(1.0)
    else:
        print("ERROR: La ventana de LDPlayer no apareció.")
        return False

    print("Ventana detectada. Esperando a que el sistema Android cargue...")
    
    # 2. Esperar elemento visual del escritorio
    while time.time() - inicio < timeout:
        pantalla = capturar_pantalla()
        if pantalla is not None:

            coords = buscar_coordenadas(img_referencia_escritorio, pantalla=pantalla)
            if coords:
                print("Escritorio de Android listo.")
                return True
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

def limpiar_anuncios_emulador():

    rect = obtener_rect_emulador(TITULO_EMULADOR)
    if not rect:
        return
    
    print("Despejando popups y anuncios iniciales del emulador...")
    pyautogui.click(rect["left"] + 200, rect["top"] + 10)
    time.sleep(20)
    
    # Dos toques de Esc para cerrar ventanas emergentes de LDPlayer
    pyautogui.press('esc')
    time.sleep(3.0)
    pyautogui.press('esc')
    time.sleep(1.0)

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
        limpiar_anuncios_emulador()
        time.sleep(60)
        cerrar_emulador()