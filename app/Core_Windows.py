# Librerías
import os
import time
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import mss

# Importar funciones visuales de Misc_Features
from Misc_Features import animar_espera, limpiar_linea_espera

# Configuración de Rutas
APP_DIR = os.path.dirname(os.path.abspath(__file__))      # Ruta de /app
ROOT_DIR = os.path.dirname(APP_DIR)                       # Ruta de la raíz (un nivel arriba)
RES_DIR = os.path.join(ROOT_DIR, "res")                   # Ruta hacia /res

# Configuración PyAutoGUI
pyautogui.PAUSE = 0.05
pyautogui.FAILSAFE = True  # Mover el mouse a una esquina de la pantalla cancela el bot en emergencia

# Conexión / Localización de la Ventana de LDPlayer
TITULO_VENTANA = "Boring Phone 14"

def obtener_rect_emulador(titulo=TITULO_VENTANA):
    """Deteccion del Emulador"""
    ventanas = gw.getWindowsWithTitle(titulo)
    if not ventanas:
        return None
    
    v = ventanas[0]
    if v.isMinimized:
        v.restore()
    return {
        "top": v.top,
        "left": v.left,
        "width": v.width,
        "height": v.height
    }

# Función de Captura de Pantalla en Windows
def capturar_pantalla():
    rect = obtener_rect_emulador()
    if not rect:
        print(f"ERROR: No se encuentra la ventana '{TITULO_VENTANA}'.")
        return None
    
    with mss.mss() as sct:
        captura = np.array(sct.grab(rect))
        # MSS captura en formato BGRA; OpenCV utiliza BGR
        return cv2.cvtColor(captura, cv2.COLOR_BGRA2BGR)

# Función de Buscar Coordenadas (Relativas a la ventana del emulador)
def buscar_coordenadas(nombre_archivo, pantalla=None, umbral=0.8):
    if pantalla is None:
        pantalla = capturar_pantalla()
    if pantalla is None:
        return None

    ruta = os.path.join(RES_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        print(f"ERROR: Archivo no encontrado: {ruta}")
        return None

    plantilla = cv2.imread(ruta)
    res = cv2.matchTemplate(pantalla, plantilla, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= umbral:
        w, h = plantilla.shape[:2][::-1]
        centro_x = max_loc[0] + w // 2
        centro_y = max_loc[1] + h // 2
        return (centro_x, centro_y)
    return None

# Función de Clic
def clic(coords, delay_despues=1.0):
    if coords:
        rect = obtener_rect_emulador()
        if not rect:
            return
        
        # Coordenada absoluta del cursor en Windows
        abs_x = rect["left"] + coords[0]
        abs_y = rect["top"] + coords[1]
        
        pyautogui.click(abs_x, abs_y)

        print(f"Clic en: {coords}")

        time.sleep(delay_despues)

# Función Esperar y Clicar
def esperar_y_clicar(
    nombre_archivo, 
    timeout=None, 
    umbral=0.8, 
    intervalo=1.0, 
    delay_antes_clic=0.5, 
    cantidad_clics=1, 
    intervalo_entre_clics=2.0,
    coords_destino=None,
    img_auxiliar=None,
    coords_img_auxiliar=None
):
    if timeout:
        print(f"Esperando '{nombre_archivo}' (máx {timeout}s)...")
        
    inicio = time.time()
    
    while True:
        pantalla = capturar_pantalla()
        
        # 1. Comprobar imagen auxiliar
        if img_auxiliar and pantalla is not None:
            coords_auxiliar = buscar_coordenadas(img_auxiliar, pantalla=pantalla, umbral=umbral)
            if coords_auxiliar:
                limpiar_linea_espera()
                punto_rescate = coords_img_auxiliar if coords_img_auxiliar is not None else coords_auxiliar
                clic(punto_rescate, delay_despues=1.5)
                inicio = time.time()

        # 2. Buscar objetivo principal
        if pantalla is not None:
            coords_encontradas = buscar_coordenadas(nombre_archivo, pantalla=pantalla, umbral=umbral)
            if coords_encontradas:
                limpiar_linea_espera()
                punto_clic = coords_destino if coords_destino is not None else coords_encontradas
                
                time.sleep(delay_antes_clic)
                
                for i in range(cantidad_clics):
                    clic(punto_clic)
                    if i < cantidad_clics - 1:
                        time.sleep(intervalo_entre_clics)
                        
                return True
            
        # 3. Timeout alcanzado
        if timeout is not None and (time.time() - inicio) >= timeout:
            limpiar_linea_espera()
            print(f"ERROR: Se acabó el tiempo, no se encontró el elemento '{nombre_archivo}'.")
            return False
        
        animar_espera("Esperando")   
        time.sleep(intervalo)

# Función genérica de ciclo con reinicio por inactividad
def ciclo_inactividad(
    objetivos,
    timeout_inactividad=60.0,
    umbral=0.8,
    intervalo=1.0,
    delay_antes_clic=0.5,
    cantidad_clics=1,
    intervalo_entre_clics=0.5,
    coords_destino=None,
):
    lista_objetivos = [objetivos] if isinstance(objetivos, str) else objetivos
    ultimo_evento = time.time()
    total_acciones = 0

    while True:
        pantalla = capturar_pantalla()
        evento_detectado = False

        if pantalla is not None:
            for nombre_archivo in lista_objetivos:
                coords_encontradas = buscar_coordenadas(nombre_archivo, pantalla=pantalla, umbral=umbral)

                if coords_encontradas:
                    limpiar_linea_espera()
                    punto_clic = coords_destino if coords_destino is not None else coords_encontradas

                    if delay_antes_clic > 0:
                        time.sleep(delay_antes_clic)

                    for i in range(cantidad_clics):
                        print(f"Clic {i + 1}/{cantidad_clics} en {punto_clic} por '{nombre_archivo}'...")
                        clic(punto_clic)
                        if i < cantidad_clics - 1:
                            time.sleep(intervalo_entre_clics)

                    total_acciones += 1
                    ultimo_evento = time.time()
                    evento_detectado = True
                    break

        if not evento_detectado and (time.time() - ultimo_evento >= timeout_inactividad):
            limpiar_linea_espera()
            break

        animar_espera("Esperando")
        time.sleep(intervalo)

# Función Clic hasta Confirmar
def clic_hasta_confirmar(
    coords_o_img_a_clicar,
    img_confirmacion,
    timeout=15.0,
    umbral=0.8,
    intervalo_reintento=3.0
):
    print("Entro a esta funcion")
    inicio = time.time()
    
    while time.time() - inicio < timeout:
        pantalla = capturar_pantalla()
        
        # 1. ¿Ya ocurrió el cambio de pantalla?
        if buscar_coordenadas(img_confirmacion, pantalla=pantalla, umbral=umbral):
            return True
            
        # 2. Si no ha cambiado, determinar el punto y volver a clicar
        if isinstance(coords_o_img_a_clicar, tuple):
            punto = coords_o_img_a_clicar
        else:
            punto = buscar_coordenadas(coords_o_img_a_clicar, pantalla=pantalla)
            
        if punto:
            clic(punto, delay_despues=0.5)
            
        time.sleep(intervalo_reintento)
        
    print(f"ERROR: No se confirmó la transición hacia '{img_confirmacion}'.")
    return False

# Función clic y confirmar
def esperar_clic_y_confirmar(
    img_o_coords_origen,
    img_confirmacion=None,
    img_desaparecer=None,
    desaparecer_origen=False,
    clic_previo=None,
    delay_clic_previo=0.5,
    timeout_aparicion=15.0,
    timeout_confirmacion=10.0,
    intervalo_reintento=1.2,
    umbral=0.8,
    delay_antes_clic=0.2
):
    if clic_previo:
        clic(clic_previo, delay_despues=delay_clic_previo)

    inicio_fase1 = time.time()
    punto_clic = None

    # ETAPA 1: Localizar / Esperar el elemento de origen
    if isinstance(img_o_coords_origen, tuple):
        punto_clic = img_o_coords_origen
    else:
        while time.time() - inicio_fase1 < timeout_aparicion:
            pantalla = capturar_pantalla()
            coords = buscar_coordenadas(img_o_coords_origen, pantalla=pantalla, umbral=umbral)
            if coords:
                punto_clic = coords
                break
            animar_espera(f"Esperando '{img_o_coords_origen}'")
            time.sleep(0.5)

        if not punto_clic:
            limpiar_linea_espera()
            return False

    limpiar_linea_espera()
    time.sleep(delay_antes_clic)

    # ETAPA 2: Bucle reactivo hasta confirmar
    inicio_fase2 = time.time()
    while time.time() - inicio_fase2 < timeout_confirmacion:
        pantalla = capturar_pantalla()
        if pantalla is not None:
            if img_confirmacion and buscar_coordenadas(img_confirmacion, pantalla=pantalla, umbral=umbral):
                return True

            if desaparecer_origen and isinstance(img_o_coords_origen, str):
                if not buscar_coordenadas(img_o_coords_origen, pantalla=pantalla, umbral=umbral):
                    return True

            if img_desaparecer and not buscar_coordenadas(img_desaparecer, pantalla=pantalla, umbral=umbral):
                return True

            if isinstance(img_o_coords_origen, str):
                punto_actual = buscar_coordenadas(img_o_coords_origen, pantalla=pantalla, umbral=umbral)
                if punto_actual:
                    punto_clic = punto_actual

        clic(punto_clic, delay_despues=0.2)
        time.sleep(intervalo_reintento)

    limpiar_linea_espera()
    print(f"ERROR: No se confirmó la acción tras clicar.")
    return False

# Deslizar nativo con el ratón de Windows adaptado a emuladores
def deslizar(inicio=(280, 800), fin=(280, 450), duracion_ms=600, delay_despues=1.2):
    rect = obtener_rect_emulador()
    if not rect:
        return
    
    start_x = rect["left"] + inicio[0]
    start_y = rect["top"] + inicio[1]
    end_x = rect["left"] + fin[0]
    end_y = rect["top"] + fin[1]
    
    # 1. Posicionarse y presionar el botón simulando el toque
    pyautogui.moveTo(start_x, start_y)
    time.sleep(0.1)
    pyautogui.mouseDown(button='left')
    time.sleep(0.15)  # Pausa para que el motor reconozca el contacto
    
    # 2. Arrastrar hacia arriba para que la lista baje
    pyautogui.moveTo(end_x, end_y, duration=duracion_ms / 1000.0)
    time.sleep(0.15)  # Pausa antes de soltar para evitar inercia descontrolada
    
    # 3. Soltar toque
    pyautogui.mouseUp(button='left')
    time.sleep(delay_despues)

# Buscar o Deslizar con coordenadas adaptadas a la nueva escala
def buscar_o_deslizar(nombre_archivo, max_deslices=5, punto_swipe_inicio=(280, 800), punto_swipe_fin=(280, 450)):
    for i in range(max_deslices):
        coords = buscar_coordenadas(nombre_archivo)
        if coords:
            return coords
        deslizar(inicio=punto_swipe_inicio, fin=punto_swipe_fin)
    print(f"ERROR: No se encontró '{nombre_archivo}'")
    return None

# Cerrar Anuncio con Banco de X
def cerrar_anuncio_banco_x(lista_imgs_x=[], timeout_anuncio=45.0):
    inicio = time.time()
    
    time.sleep(30.0)
    
    while time.time() - inicio < timeout_anuncio:
        pantalla = capturar_pantalla()
        if pantalla is not None:
            for img_x in lista_imgs_x:
                coords_x = buscar_coordenadas(img_x, pantalla=pantalla)
                if coords_x:
                    clic(coords_x, delay_despues=2.0)
                    return True
    
    print("\nNo se detectó ninguna punto de cierre conocido.")
    input("Cierra el anuncio a mano y pulsa [ENTER]...")
    return False

# Función para cerrar el app
def cerrar_app(nombre_app, img_borrar_todo="BT.png"): #BT - Borrar Todo
    rect = obtener_rect_emulador()
    if not rect:
        return False

    # Enfocar emulador y presionar F2
    pyautogui.click(rect["left"] + 200, rect["top"] + 10)
    time.sleep(0.5)
    pyautogui.press('f2')
    time.sleep(1.5)

    # Deslizar desde el centro de izquierda a derecha
    deslizar(inicio=(120, 500), fin=(440, 500), duracion_ms=500, delay_despues=1.0)

    # Buscar y clicar directo al centro de la imagen
    pantalla = capturar_pantalla()
    coords_centro = buscar_coordenadas(img_borrar_todo, pantalla=pantalla)
    if coords_centro:
        clic(coords_centro, delay_despues=1.5)
        print (f"Aplicacion {nombre_app} Cerrada")
        return True

    pyautogui.press('esc')
    return False