import time
from Core_Windows import esperar_y_clicar, ciclo_inactividad, clic, capturar_pantalla, buscar_coordenadas, buscar_o_deslizar, cerrar_anuncio_banco_x, cerrar_app, clic_hasta_confirmar
from Misc_Features import animar_espera, limpiar_linea_espera

APLICACION = "Digimon Up"

def ciclo_granja_de_carne(
    img_sel="G03.png", # G03 - Granja de Carne Boton Seleccionar
    img_pal="G02.png", # G02 - Granja de Carne Pala
    img_reg="G04.png", # G04 - Granja de Carne Boton Regar
    timeout=5.0
):
    inicio = time.time()

    while time.time() - inicio < timeout:
        pantalla = capturar_pantalla()

        coords_pal = buscar_coordenadas(img_pal, pantalla=pantalla)
        if coords_pal:
            clic(coords_pal, delay_despues=1.0)
            
            esperar_y_clicar(img_sel, timeout=5.0, delay_antes_clic=0.5)
            return

        coords_sel = buscar_coordenadas(img_sel, pantalla=pantalla)
        if coords_sel:
            clic(coords_sel, delay_despues=1.0)
            return

        coords_reg = buscar_coordenadas(img_reg, pantalla=pantalla)
        if coords_reg:
            clic((280, 895), delay_despues=1.0)
            return

        time.sleep(0.3)

    return None


def ciclo_calabozo(
    img_tarjeta_calabozo,
    img_bttn_intentar="015.png",          # 015 - Botón Intentar o Emparejar
    img_bttn_claqueta="017.png",          # 017 - Ícono limpio de Claqueta
    img_claqueta_agotada="016.png",      # 016 - Texto 0/2 morado
    img_sin_anuncios="018.png",           # 018 - Aviso sin anuncios
    img_bttn_confirmar_salir=None,        # Opcional: para confirmaciones como Defensa en Red
    img_confirmacion="032.png",
    banco_x_anuncios=[],
    ver_anuncios=False
):
    coords_tarjeta = buscar_o_deslizar(img_tarjeta_calabozo)
    if not coords_tarjeta:
        return
    
    clic(coords_tarjeta, delay_despues=2.0)

    # Bucle principal
    while True:
        pantalla = capturar_pantalla()

        coords_intentar = buscar_coordenadas(img_bttn_intentar, pantalla=pantalla)
        if coords_intentar:
            clic(coords_intentar, delay_despues=2.0)
            time.sleep(1.0)
            clic(coords_intentar, delay_despues=2.0)
            esperar_y_clicar("014.png", timeout=120, cantidad_clics=2, intervalo_entre_clics=1.0)
            time.sleep(4.0)
            print("Calabozo Terminado")
            continue

        coords_claqueta = buscar_coordenadas(img_bttn_claqueta, pantalla=pantalla)
        if coords_claqueta:
            if not ver_anuncios:
                print("Ciclo de Calabozo Terminado 1")
                break

            if buscar_coordenadas(img_claqueta_agotada, pantalla=pantalla, umbral=0.95):
                print("Ciclo de Calabozo Terminado 2")
                break

            clic(coords_claqueta, delay_despues=2.0)
            clic(coords=(350, 615), delay_despues=0.8)

            pantalla_aviso = capturar_pantalla()
            if buscar_coordenadas(img_sin_anuncios, pantalla=pantalla_aviso, umbral=0.85):
                break

            cerrar_anuncio_banco_x(lista_imgs_x=banco_x_anuncios)

            time.sleep(4.0)

            clic_hasta_confirmar(coords_o_img_a_clicar=(280, 975), img_confirmacion=img_confirmacion)
            continue

        time.sleep(1.5)

    clic_hasta_confirmar(coords_o_img_a_clicar=(280, 975), img_confirmacion=img_confirmacion, umbral=1.00)

    if img_bttn_confirmar_salir:
        time.sleep(1.0)
        pantalla_cierre = capturar_pantalla()
        coords_confirmar = buscar_coordenadas(img_bttn_confirmar_salir, pantalla=pantalla_cierre)
        if coords_confirmar:
            clic(coords_confirmar, delay_despues=1.5)
    print("Saliendo del Calabozo")

def ciclo_idle(
    tiempo_total_min=15,
    img_bttn_vender="031.png",           # 031 - Botón Vender (Referencia de menú abierto)
    img_flechas_arriba="029.png",        # 029 - Flecha verde hacia arriba (Mejora)
    img_bttn_equipar="030.png",          # 030 - Botón Equipar
    img_alerta_exclamacion="028.png",    # 028 - Signo de Exclamación
    coords_clic_alerta=(280, 850),       # Coordenada donde pulsar tras ver la exclamación
    imgs_intrusivas=["E01.png", "E02.png"],
    coords_cerrar_intrusivas=(280, 975)
):
    tiempo_limite = time.time() + (tiempo_total_min * 60)

    while time.time() < tiempo_limite:
        minutos_restantes = int((tiempo_limite - time.time()) // 60)
        segundos_restantes = int((tiempo_limite - time.time()) % 60)
        animar_espera(f"Vigilando [{minutos_restantes:02d}:{segundos_restantes:02d}]")

        pantalla = capturar_pantalla()
        if pantalla is None:
            time.sleep(1.0)
            continue

        # 1. ¿El menú ya se abrió automáticamente (detectando el botón Vender)?
        coords_vender = buscar_coordenadas(img_bttn_vender, pantalla=pantalla)
        if coords_vender:
            limpiar_linea_espera()
            print("Holograma Encontrado")

            # Comprobar si hay mejora con flechas verdes
            if buscar_coordenadas(img_flechas_arriba, pantalla=pantalla, umbral=0.85):
                esperar_y_clicar(img_bttn_equipar, timeout=10, delay_antes_clic=0.3)
                print("Holograma Equipado")
                time.sleep(1.2)

            # Vender objeto
            clic(coords_vender, delay_despues=1.5)
            print("Holograma Vendido")
            continue

        # 2. Manejo de pantallas intrusivas (E01 - Fase Fallida, E02 - Time Sale)
        intrusiva_encontrada = False
        for img_e in imgs_intrusivas:
            if buscar_coordenadas(img_e, pantalla=pantalla):
                limpiar_linea_espera()
                clic(coords_cerrar_intrusivas, delay_despues=1.5)
                intrusiva_encontrada = True
                break
        
        if intrusiva_encontrada:
            continue

        # 3. ¿Apareció la exclamación para abrir el menú manualmente?
        if buscar_coordenadas(img_alerta_exclamacion, pantalla=pantalla, umbral=0.70):
            limpiar_linea_espera()
            clic(coords_clic_alerta, delay_despues=4.0)
            continue

        time.sleep(1.0)

    print("Saliendo del ciclo IDLE")
    limpiar_linea_espera()

def iniciar_app():
    print("Buscando Logo de Digimon Up")
    esperar_y_clicar("001.png", timeout=30) # 001 - Logo Digimon Up
    print("Click en Logo de Digimon Up")

    print("Buscando Start")
    esperar_y_clicar("002.png", delay_antes_clic=3.0, timeout=300, coords_destino=(280, 700), intervalo=3.0, cantidad_clics=2, umbral=0.70) # 002 - Boton Start
    print("Click en Start")
    return None

def anuncios():
    print("Buscando Checkbox de Dejar de Mostrar Hoy")
    esperar_y_clicar("010.png", delay_antes_clic=3.0, timeout=20, cantidad_clics=2) #010 - Checkbox Dejar de Mostrar Hoy
    print("Click en Checkbox o Omitido por haber hecho click antes")
    # Cambiar esta funcion por clic_hasta_confirmar
    
    print("Clicks en confirmar para quitar anuncios destacados")
    ciclo_inactividad("011.png", timeout_inactividad=5.0) # 011 - Boton Confirmar Anuncios Destacados

    print("Quitar el Tablon de Anuncios")
    esperar_y_clicar("012.png", coords_destino=(280, 975), timeout=30, cantidad_clics=3, intervalo_entre_clics=3.0, delay_antes_clic=3.0) # 012 - Tablon de Avisos
    return None

def recompensas():
    #Verificacion de Ventanas Emergentes
    ciclo_inactividad(["E01.png", "E02.png"], timeout_inactividad=10.0, coords_destino=(280, 895)) # E01 - Fase Fallida, E02 - Time Sale

    print("Clic en la Caja de Recompensas")
    clic(coords=(80, 715), delay_despues=1.0) #Cordenadas de la Caja de Recompensas

    print("Dar clic en obtener recompensas")
    esperar_y_clicar("005.png", timeout=20, img_auxiliar="E01.png", coords_img_auxiliar=(280, 895), umbral=0.92) # 005 - Boton Obtener Recompensas, E01 - Fase Fallida

    time.sleep(3)

    print("Cerrar ventana Obtener Recompensas")
    esperar_y_clicar("006.png", # 006 - Texto Toca para Cerrar
                            timeout=20, img_auxiliar="E01.png", # E01 - Fase Fallida
                            coords_img_auxiliar=(280, 975), cantidad_clics=2, 
                            intervalo_entre_clics=5.0)
    return None

def hologramas_automaticos():
    print("Dar clic en el boton de Apertura de Hologramas Automaticos")
    esperar_y_clicar("007.png", timeout=60) # 009 - Boton A Pull Automatico
    return None

def granja_de_carne():
    print("Clic en el menu de Explorar")
    clic(coords=(415, 980), delay_despues=3.0) #Cordenadas Boton Explorar

    print("Clic en Granjas de Carne")
    clic(coords=(165, 510), delay_despues=3.0) #Cordenadas Boton Granjas de Carne

    #Clic a la granja Numero 1
    print("Inicio de Granja de Carne 1")
    clic(coords=(180, 625))
    ciclo_granja_de_carne()
    time.sleep(3)
    print("Inicio de Granja de Carne 1")

    #Clic a la granja Numero 2
    print("Inicio de Granja de Carne 2")
    clic(coords=(180, 775))
    ciclo_granja_de_carne()
    time.sleep(3)
    print("Inicio de Granja de Carne 2")

    #Clic a la granja Numero 3
    print("Inicio de Granja de Carne 3")
    clic(coords=(385, 775))
    ciclo_granja_de_carne()
    time.sleep(3)
    print("Inicio de Granja de Carne 3")

    print("Cerrar Granjas de Carne")
    esperar_y_clicar("013.png", timeout=60) # 013 - Granja de Carne Boton X
    return None

def calabozos():
    print("Clic en el menu Calabozo")
    clic(coords=(205, 980), delay_despues=2.0)

    print("Inicio Calabozo de Devimon")
    ciclo_calabozo("C01.png") # C01 - Calabozo Devimon
    time.sleep(3)

    print("Inicio Calabozo de Bakemon")
    ciclo_calabozo("C02.png") # C02 - Calabozo Bakemon
    time.sleep(3)

    print("Inicio Digifabrica")
    ciclo_calabozo("C03.png") # C03 - Digifabrica
    time.sleep(3)

    print("Inicio Defensa en Red")
    ciclo_calabozo("C04.png", img_bttn_confirmar_salir="020.png", img_bttn_intentar="019.png", img_confirmacion="020.png") # C04 - Defensa en Red
    time.sleep(3)

    print("Inicio Mar Metalico")
    ciclo_calabozo("C05.png") # C05 - Mar Metalico
    time.sleep(3)
    return None

def sorteos():
    print("Ir a Pantalla Principal")
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global

    ciclo_inactividad(["E01.png", "E02.png"], timeout_inactividad=10.0, coords_destino=(280, 895)) # E01 - Fase Fallida, E02 - Time Sale

    print("Clic en Sorteos")
    clic(coords=(475, 540), delay_despues=3.0) # Icono de Sorteo

    print("Pestaña de Sorteos Normales")
    esperar_y_clicar("021.png", timeout=20) # 021 - Boton Sorteo Normal

    time.sleep(3)

    clic(coords=(90, 220), delay_despues=3.0) #Estado Default

    print("Clic en 35 Sorteos de Cartas de Habilidad")
    esperar_y_clicar("022.png", timeout=20) # 022 - Boton Sorteo x 35

    time.sleep(3)

    print("Cerrar Sorteo")
    esperar_y_clicar("024.png", timeout=20) # 024 - Boton Cerrar

    time.sleep(3)

    esperar_y_clicar("023.png", timeout=20) # 023 - Digimon de Apoyo

    time.sleep(3)

    print("Clic en 35 Sorteos de Digimon de Apoyo")
    esperar_y_clicar("022.png", timeout=20) # 022 - Boton Sorteo x 35

    time.sleep(3)

    print("Cerrar Sorteo")
    esperar_y_clicar("024.png", timeout=20) # 024 - Boton Cerrar

    time.sleep(3)

    print("Cerrar Menu de Sorteos")
    esperar_y_clicar("024.png", timeout=20, umbral=0.70) # 024 - Boton Cerrar

    time.sleep(3)
    return None

def jcj():
    print("Ir a Pantalla Principal")
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    time.sleep(1)
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global

    #Verificacion de Ventanas Emergentes
    ciclo_inactividad(["E01.png", "E02.png"], timeout_inactividad=10.0, coords_destino=(280, 895)) # E01 - Fase Fallida, E02 - Time Sale

    time.sleep(3)

    print("Clic en JcJ")
    clic(coords=(90, 170), delay_despues=3.0) #Cordenadas Boton JcJ

    for i in range(3):
        print("Clic en Entrar")
        esperar_y_clicar("025.png", timeout=20) # 025 - Boton Entrar Combates

        time.sleep(3)
        print("Batalla Posicion 5")
        clic(coords=(400, 625), delay_despues=3.0) # Coordenadas Boton Intentar Batalla Posicion 5

        print("Finalizar Combate")
        esperar_y_clicar("026.png", timeout=120, cantidad_clics=2) # 026 - Texto Tocar para Cerrar

        time.sleep(5)

    print("Boton Cerrar")
    esperar_y_clicar("013.png", timeout=20, cantidad_clics=2) # 013 - Boton Cerrar

    return None

def gemas_diarias():
    print("Ir a Pantalla Principal")
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    time.sleep(1)
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global

    ciclo_inactividad(["E01.png", "E02.png"], timeout_inactividad=10.0, coords_destino=(280, 895)) # E01 - Fase Fallida, E02 - Time Sale
    time.sleep(3)

    print("Menu de Tienda")
    clic(coords=(475, 965), delay_despues=3.0) #Cordenadas Boton Tienda
    time.sleep(3)

    print("Clic en Seccion Divisa Premium")
    clic(coords=(220, 905), delay_despues=3.0) #Cordenadas Apartado Divisa Premium
    time.sleep(3)

    print("Clic en Gemas Diarias")
    clic(coords=(180, 715), delay_despues=3.0) #Cordenadas Gemas Diarias
    time.sleep(3)

    print("Clic en el Boton Gratis")
    esperar_y_clicar("027.png", timeout=20) # 027 - Boton Gratis
    time.sleep(5)

    print("Ir a Pantalla Principal")
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    time.sleep(1)
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    return None

def recibir_recompensas_misiones():
    print("Ir a Pantalla Principal")
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    time.sleep(1)
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global

    ciclo_inactividad(["E01.png", "E02.png"], timeout_inactividad=10.0, coords_destino=(280, 895)) # E01 - Fase Fallida, E02 - Time Sale

    print("Clic en Misiones")
    clic(coords=(470, 175), delay_despues=3.0) #Cordenadas Boton Misiones
    time.sleep(3)

    print("Clic en Seccion Misiones Diarias")
    clic(coords=(280, 810), delay_despues=3.0) #Cordenadas Apartado Misiones Diarias
    time.sleep(3)

    print("Clic en Boton Recibir")
    clic(coords=(415, 590), delay_despues=3.0) #Cordenadas Boton Recibir
    time.sleep(3)

    print("Aceptar")
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    time.sleep(1)

    print("Clic en Las Recompensas Principales")
    clic(coords=(155, 310), delay_despues=3.0) #Cordenadas Recompensas Principales
    time.sleep(3)

    print("Aceptar")
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    time.sleep(1)

    print("Ir a Pantalla Principal")
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    time.sleep(1)
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    return None

def digimon_up_bot():
    
    #Fase 1: Iniciar Aplicacion en el Emuladior y Dar Start al Juego
    print("Fase 1")
    iniciar_app()
    
    #Fase 2: Quitar Noticias Destacadas y Tablon de Anuncios
    print("Fase 2")
    anuncios()
    time.sleep(5)
    
    #Fase 3: Recoger Recompensas
    print("Fase 3")
    recompensas()
    time.sleep(5)

    #Fase 4: Activar Automatico
    print("Fase 4")
    hologramas_automaticos()
    time.sleep(5)

    #Fase 5: Granja de Carne
    print("Fase 5")
    granja_de_carne()
    time.sleep(5)
    
    #Fase 6: Calabozos
    print("Fase 6")
    calabozos()
    time.sleep(5)

    #Fase 7: Sorteos
    print("Fase 7")
    sorteos()
    time.sleep(5)

    #Fase 8: Jugador contra Jugador
    print("Fase 8")
    jcj()
    time.sleep(5)

    #Fase 9: Recoger Gemas Diarias
    print("Fase 9")
    gemas_diarias()
    time.sleep(5)

    #Fase 10: cliclo idle
    print("Fase 10")
    ciclo_idle()
    time.sleep(5)

    #Fase 11: Recoger
    print("Fase 11")
    recibir_recompensas_misiones()
    time.sleep(5)

    cerrar_app(nombre_app=APLICACION)

    print("\nRuta del Bot de Digimon Up Finalizada")
# Ejecutar
digimon_up_bot()