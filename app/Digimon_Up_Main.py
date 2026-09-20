import time
from Core_Windows import (esperar_y_clicar, 
                          ciclo_inactividad, 
                          clic, capturar_pantalla, 
                          buscar_coordenadas, 
                          buscar_o_deslizar, 
                          cerrar_anuncio_banco_x, 
                          abrir_app,
                          cerrar_app, 
                          clic_hasta_confirmar, 
                          esperar_clic_y_confirmar)
from Misc_Features import animar_espera, limpiar_linea_espera, iniciar_logger

APLICACION = "Digimon Up"

def ciclo_granja_de_carne(
    coords_parcela=None,
    img_sel="G03.png",  # G03 - Botón Seleccion
    img_pal="G02.png",  # G02 - Icono Pala
    img_reg="G04.png",  # G03 - Boton Regar
    coords_bttn_reg=(280, 895),
    timeout=5.0
):
    if coords_parcela:
        clic(coords_parcela, delay_despues=0.8)

    inicio = time.time()
    while time.time() - inicio < timeout:
        pantalla = capturar_pantalla()
        if pantalla is None:
            time.sleep(0.3)
            continue

        # 1. Caso Pala
        if buscar_coordenadas(img_pal, pantalla=pantalla):
            print("Recolectando...")
            if esperar_clic_y_confirmar(img_pal, img_confirmacion=img_sel, timeout_confirmacion=4.0):
                esperar_clic_y_confirmar(img_sel, desaparecer_origen=True, timeout_confirmacion=4.0)
            return

        # 2. Caso Menú ya abierto
        if buscar_coordenadas(img_sel, pantalla=pantalla):
            print("Seleccionando semilla...")
            esperar_clic_y_confirmar(img_sel, desaparecer_origen=True, timeout_confirmacion=4.0)
            return

        # 3. Caso Regar
        if buscar_coordenadas(img_reg, pantalla=pantalla):
            print("Regando cultivo...")
            esperar_clic_y_confirmar(coords_bttn_reg, img_desaparecer=img_reg, timeout_confirmacion=4.0)
            return

        time.sleep(0.3)


def ciclo_calabozo(
    img_tarjeta_calabozo,
    img_bttn_intentar="015.png",          # 015 - Botón Intentar o Emparejar
    img_bttn_claqueta="017.png",          # 017 - Ícono limpio de Claqueta
    img_claqueta_agotada="016.png",      # 016 - Texto 0/2 morado
    img_sin_anuncios="018.png",           # 018 - Aviso sin anuncios
    img_bttn_confirmar_salir=None,        # Opcional: para confirmaciones como Defensa en Red
    umbral_confirmacion=1.00,
    img_confirmacion="032.png",
    banco_x_anuncios=[],
    ver_anuncios=False
):
    coords_tarjeta = buscar_o_deslizar(img_tarjeta_calabozo)
    if not coords_tarjeta:
        return
    
    esperar_clic_y_confirmar(img_o_coords_origen=img_tarjeta_calabozo, desaparecer_origen=True)

    # Bucle principal
    while True:
        pantalla = capturar_pantalla()

        coords_intentar = buscar_coordenadas(img_bttn_intentar, pantalla=pantalla)
        if coords_intentar:
            esperar_clic_y_confirmar(img_o_coords_origen=img_bttn_intentar, desaparecer_origen=True)
            esperar_y_clicar("014.png", timeout=120, cantidad_clics=2, intervalo_entre_clics=0.5)
            time.sleep(4.0)
            print("Calabozo Terminado")
            continue

        coords_claqueta = buscar_coordenadas(img_bttn_claqueta, pantalla=pantalla)
        if coords_claqueta:
            if not ver_anuncios:
                print("Ciclo de Calabozo Terminado")
                break

            if buscar_coordenadas(img_claqueta_agotada, pantalla=pantalla, umbral=0.95):
                print("Ciclo de Calabozo Terminado")
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

    clic_hasta_confirmar(coords_o_img_a_clicar=(280, 975), img_confirmacion=img_confirmacion, umbral=umbral_confirmacion)

    if img_bttn_confirmar_salir:
        time.sleep(1.0)
        pantalla_cierre = capturar_pantalla()
        coords_confirmar = buscar_coordenadas(img_bttn_confirmar_salir, pantalla=pantalla_cierre)
        if coords_confirmar:
            clic(coords_confirmar, delay_despues=1.5)
    print("Saliendo del Calabozo")

def ciclo_idle(
    tiempo_total_min=15,
    imgs_bttn_vender=["031.png", "034.png"],     # AHORA ES UNA LISTA: ["Vender normal", "Vender Todo"]
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

        coords_vender = None
        img_encontrada = None
        
        for img_vender in imgs_bttn_vender:
            coords_actual = buscar_coordenadas(img_vender, pantalla=pantalla)
            if coords_actual:
                coords_vender = coords_actual
                img_encontrada = img_vender
                break # Si encuentra uno, rompe el ciclo for y guarda las coordenadas

        if coords_vender:
            limpiar_linea_espera()
            print(f"Holograma(s) Encontrado(s) - Botón detectado: {img_encontrada}")

            # Comprobar si hay mejora con flechas verdes
            if buscar_coordenadas(img_flechas_arriba, pantalla=pantalla, umbral=0.85):
                esperar_y_clicar(img_bttn_equipar, timeout=10, delay_antes_clic=0.3)
                print("Holograma Equipado")
                time.sleep(1.2)

            # Vender objeto(s) usando la coordenada del botón que se encontró
            clic(coords_vender, delay_despues=1.5)
            print("Holograma(s) Vendido(s)")
            continue

        # Manejo de pantallas intrusivas (E01 - Fase Fallida, E02 - Time Sale)
        intrusiva_encontrada = False
        for img_e in imgs_intrusivas:
            if buscar_coordenadas(img_e, pantalla=pantalla):
                limpiar_linea_espera()
                clic(coords_cerrar_intrusivas, delay_despues=1.5)
                intrusiva_encontrada = True
                break
        
        if intrusiva_encontrada:
            continue

        # Aparicion de Exclamacion
        if buscar_coordenadas(img_alerta_exclamacion, pantalla=pantalla, umbral=0.70):
            limpiar_linea_espera()
            clic(coords_clic_alerta, delay_despues=4.0)
            continue

        time.sleep(1.0)

    print("Saliendo del ciclo IDLE")
    limpiar_linea_espera()

def iniciar_app(timeout_carga=120.0):
    
    # Funcion de estabilizacion de inicio
    if not abrir_app(nombre_app=APLICACION, img_icono_app="001.png", max_intentos=5):
        return False

    # Esperar a que pase el logo y llegue a "Start"
    print("\nEsperando la pantalla de Start de Digimon Up...")
    inicio_espera_start = time.time()
    start_encontrado = False
    
    while time.time() - inicio_espera_start < timeout_carga:
        pantalla = capturar_pantalla()
        if pantalla is None:
            time.sleep(1.0)
            continue

        if buscar_coordenadas("002.png", pantalla=pantalla, umbral=0.70):
            print("Pantalla de Start alcanzada con éxito.")
            clic((280, 700), delay_despues=3.0)
            clic((280, 700), delay_despues=3.0)  # Clic en Start
            start_encontrado = True
            break

        if buscar_coordenadas("SA.png", pantalla=pantalla):
            print("ALERTA: El juego se cerró de forma tardía esperando el Start.")
            return False

        animar_espera(f"Cargando Start ({int(time.time() - inicio_espera_start)}s)")
        time.sleep(2.0)

    if not start_encontrado:
        limpiar_linea_espera()
        print("ERROR: Timeout esperando la pantalla de Start.")
        return False

    # Confirmar que la carga terminó
    print("\nEsperando a entrar al juego tras pulsar Start...")
    
    # Define las imágenes que te confirman que ya estás dentro del juego
    imgs_confirmacion_ingreso = ["010.png", "012.png"] # Ej: El tablon de anuncios o texto de dejar de mostrar hoy
    inicio_espera_ingreso = time.time()
    
    while time.time() - inicio_espera_ingreso < timeout_carga:
        pantalla = capturar_pantalla()
        if pantalla is None:
            time.sleep(1.0)
            continue

        # Revisamos si aparece cualquiera de las imágenes que confirman el ingreso
        for img in imgs_confirmacion_ingreso:
            if buscar_coordenadas(img, pantalla=pantalla):
                limpiar_linea_espera()
                print(f"Carga finalizada con éxito. Se detectó '{img}'.")
                return True

        # Si el juego crashea
        if buscar_coordenadas("SA.png", pantalla=pantalla):
            limpiar_linea_espera()
            print("ALERTA CRÍTICA: El juego crasheó durante la barra de carga tras pulsar Start.")
            return False

        animar_espera(f"Cargando ingreso al juego ({int(time.time() - inicio_espera_ingreso)}s)")
        time.sleep(2.0)

    limpiar_linea_espera()
    print("ERROR: Timeout esperando ingresar al juego tras pulsar Start (posible congelamiento).")
    return False

def anuncios():
    print("Determinando estado inicial de anuncios...")
    
    # Capturamos la pantalla una sola vez
    pantalla_inicial = capturar_pantalla()
    
    if pantalla_inicial is not None:
        if buscar_coordenadas("012.png", pantalla=pantalla_inicial):
            print("Tablón de anuncios detectado directamente. Saltando pasos previos.")
            
        elif buscar_coordenadas("010.png", pantalla=pantalla_inicial):
            print("Buscando Checkbox de Dejar de Mostrar Hoy")
            esperar_clic_y_confirmar(
                img_o_coords_origen="010.png",
                img_confirmacion="033.png",
                timeout_aparicion=40.0,
                timeout_confirmacion=6.0,
                intervalo_reintento=1.0,
                delay_antes_clic=1.0
            )
            print("Checkbox marcado con éxito.")

            print("Clicks en confirmar para quitar anuncios destacados")
            ciclo_inactividad("011.png", timeout_inactividad=5.0) # 011 - Boton Confirmar Anuncios Destacados
            
        else:
            print("ALERTA: No se detectó ni el checkbox ni el tablón en la captura inicial.")
            
    # Acción final: Cierre del tablón (siempre se ejecuta)
    print("Quitar el Tablon de Anuncios")
    esperar_y_clicar("012.png", coords_destino=(280, 975), timeout=30, cantidad_clics=3, intervalo_entre_clics=3.0, delay_antes_clic=3.0) 
    
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
    clic(coords=(415, 980), delay_despues=2.0)

    print("Clic en Granjas de Carne")
    clic(coords=(165, 510), delay_despues=2.5)

    parcelas = [
        ("Granja 1", (180, 625)),
        ("Granja 2", (180, 775)),
        ("Granja 3", (385, 775)),
        ("Granja 4", (385, 625))
    ]

    for nombre, coords in parcelas:
        print(f"Atendiendo {nombre}...")
        ciclo_granja_de_carne(coords_parcela=coords)

    print("Cerrar Granjas de Carne")
    esperar_y_clicar("013.png", timeout=10)

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
    ciclo_calabozo("C04.png", 
                   img_bttn_confirmar_salir="020.png", 
                   img_bttn_intentar="019.png", 
                   img_confirmacion="020.png", 
                   umbral_confirmacion=0.80) # C04 - Defensa en Red
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
    clic(coords=(280, 975), delay_despues=2.0) #Cordenadas Boton Global
    time.sleep(1)
    clic(coords=(280, 975), delay_despues=2.0) #Cordenadas Boton Global

    #Verificacion de Ventanas Emergentes
    ciclo_inactividad(["E01.png", "E02.png"], timeout_inactividad=10.0, coords_destino=(280, 895)) # E01 - Fase Fallida, E02 - Time Sale

    time.sleep(3)

    print("Clic en JcJ")
    clic(coords=(90, 170), delay_despues=3.0) #Cordenadas Boton JcJ

    for i in range(3):
        print("Clic en Entrar")
        esperar_clic_y_confirmar(img_o_coords_origen="025.png", desaparecer_origen=True, intervalo_reintento=3.0) # 025 - Boton Entrar Combates

        time.sleep(3)
        print("Batalla Posicion 5")
        clic(coords=(400, 625), delay_despues=3.0) # Coordenadas Boton Intentar Batalla Posicion 5

        print("Finalizar Combate")
        esperar_clic_y_confirmar(img_o_coords_origen="026.png", desaparecer_origen=True, intervalo_reintento=3.0, timeout_aparicion=60.0) # 026 - Texto Tocar para Cerrar

        time.sleep(5)

    print("Boton Cerrar")
    esperar_clic_y_confirmar(img_o_coords_origen="013.png", desaparecer_origen=True, intervalo_reintento=3.0) # 013 - Boton Cerrar

    return None

def gemas_diarias():
    print("Ir a Pantalla Principal")
    clic(coords=(280, 975), delay_despues=2.0) #Cordenadas Boton Global
    time.sleep(1)
    clic(coords=(280, 975), delay_despues=2.0) #Cordenadas Boton Global

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

def cobrar_todas_las_misiones():
    
    print("Clics en todos los botones Recibir disponibles")
    while True:
        pantalla = capturar_pantalla()
        if pantalla is None:
            time.sleep(0.5)
            continue
            
        coords_recibir = buscar_coordenadas("035.png", pantalla=pantalla)
        if coords_recibir:
            clic(coords_recibir, delay_despues=2.5) # Clic al botón recibir
            
            # Clic para "Aceptar" la ventana de los objetos obtenidos
            clic(coords=(280, 975), delay_despues=1.5) 
        else:
            print("No se detectan más botones Recibir.")
            break

def recibir_recompensas_misiones():
    print("Ir a Pantalla Principal")
    clic(coords=(280, 975), delay_despues=2.0) #Cordenadas Boton Global
    time.sleep(1)
    clic(coords=(280, 975), delay_despues=2.0) #Cordenadas Boton Global

    ciclo_inactividad(["E01.png", "E02.png"], timeout_inactividad=10.0, coords_destino=(280, 895)) # E01 - Fase Fallida, E02 - Time Sale

    print("Clic en Misiones")
    clic(coords=(470, 175), delay_despues=3.0) #Cordenadas Boton Misiones
    time.sleep(3)

    # Misiones Diarias
    print("Clic en Seccion Misiones Diarias")
    esperar_clic_y_confirmar(
        img_o_coords_origen="036.png", 
        img_confirmacion="039.png", 
        timeout_aparicion=10.0, 
        timeout_confirmacion=10.0,
        delay_antes_clic=1.0
    )
    time.sleep(1)
    
    cobrar_todas_las_misiones()
    
    # Este clic de recompensa principal lo mantenemos tal cual lo diseñaste
    print("Clic en Las Recompensas Principales")
    clic(coords=(155, 310), delay_despues=3.0) #Cordenadas Recompensas Principales
    time.sleep(3)
    print("Aceptar")
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    time.sleep(1)

    # Colección
    print("Clic en Seccion Coleccion")
    esperar_clic_y_confirmar(
        img_o_coords_origen="037.png", 
        img_confirmacion="040.png", 
        timeout_aparicion=10.0, 
        timeout_confirmacion=10.0,
        delay_antes_clic=1.0
    )
    time.sleep(1)
    
    cobrar_todas_las_misiones()

    # Misiones EX
    print("Clic en Seccion Misiones EX")
    esperar_clic_y_confirmar(
        img_o_coords_origen="038.png", 
        img_confirmacion="041.png", 
        timeout_aparicion=10.0, 
        timeout_confirmacion=10.0,
        delay_antes_clic=1.0
    )
    time.sleep(1)
    
    cobrar_todas_las_misiones()

    print("Ir a Pantalla Principal")
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    time.sleep(1)
    clic(coords=(280, 975), delay_despues=3.0) #Cordenadas Boton Global
    
    return None

def digimon_up_bot():
    
    #Fase 1: Iniciar Aplicacion en el Emulador y Dar Start al Juego
    print(f"Fase 1: Iniciar {APLICACION} y Inicio del Juego")
    if not iniciar_app():
        print("Fallo Reintenta el Inicio del Script Manual")
        return
    
    #Fase 2: Quitar Noticias Destacadas y Tablon de Anuncios
    print("Fase 2: Pop-ups y Noticias")
    anuncios()
    time.sleep(5)
    
    #Fase 3: Recoger Recompensas
    print("Fase 3: Caja de Recompensas")
    recompensas()
    time.sleep(5)

    #Fase 4: Activar Automatico
    print("Fase 4: Capsula de Hologramas Automatico")
    hologramas_automaticos()
    time.sleep(5)

    #Fase 5: Granja de Carne
    print("Fase 5: Granjas de Carne")
    granja_de_carne()
    time.sleep(5)
    
    #Fase 6: Calabozos
    print("Fase 6: calabozos")
    calabozos()
    time.sleep(5)

    #Fase 7: Sorteos
    print("Fase 7: Sorteos")
    sorteos()
    time.sleep(5)

    #Fase 8: Jugador contra Jugador
    print("Fase 8: Jugador contra Jugador")
    jcj()
    time.sleep(5)

    #Fase 9: Recoger Gemas Diarias
    print("Fase 9: Gemas Diarias")
    gemas_diarias()
    time.sleep(5)

    #Fase 10: ciclo idle
    print("Fase 10: Ciclo IDLE")
    ciclo_idle()
    time.sleep(5)

    #Fase 11: Recoger Recompensas Diarias
    print("Fase 11: Misiones")
    recibir_recompensas_misiones()
    time.sleep(5)

    cerrar_app(nombre_app=APLICACION)

    print("\nRuta del Bot de Digimon Up Finalizada")
# Ejecutar
if __name__ == "__main__":
    iniciar_logger(prefijo="Digimon_Up")
    digimon_up_bot()