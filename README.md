# Digimon_Up_PyBot

Bot de automatización modular y desatendido para el juego móvil *Digimon Up* en emuladores LDPlayer sobre Windows. Utiliza visión por computadora con OpenCV para reconocimiento de patrones visuales y control de interfaz gráfica.

---

## Tabla de Contenidos
* [Descripción General](#descripción-general)
* [Estructura del Proyecto](#estructura-del-proyecto)
* [Requisitos Previos](#requisitos-previos)
* [Instalación](#instalación)
* [Uso](#uso)
  * [Rama main (Modo Directo)](#rama-main-modo-directo)
  * [Rama cli (Modo Automatizado)](#rama-cli-modo-automatizado)
* [Explicación del Código](#explicación-del-código)
  * [Archivos Core](#archivos-core)
  * [Archivos CLI](#archivos-cli)
* [Historial de Versiones](#historial-de-versiones)

---

## Descripción General
Este software permite ejecutar de forma autónoma las rutinas diarias de *Digimon Up*, tales como recolección de granjas, calabozos diarios, batallas JcJ, canje de recompensas y ciclos inactivos (*IDLE*). Cuenta con mecanismos de recuperación ante caídas del emulador, manejo de bloqueos por popups y registro de eventos (*logging*) en disco.

---

## Estructura del Proyecto

El repositorio está organizado en dos ramas de trabajo:

### Base

```text
Digimon_Up_PyBot/
├── app/
│   ├── Core_Windows.py            # Motor de visión y control de ventana
│   ├── Digimon_Up_Main.py         # Rutinas y lógica del juego
│   └── Misc_Features.py           # Logger y utilidades de consola
├── res/                           # Recursos gráficos (plantillas PNG para coincidencia)
├── logs/                          # Registros generados automáticamente en tiempo de ejecución
└── .gitignore                     # Filtros de exclusión de Git
```

### CLI

```text
Digimon_Up_PyBot/
├── app/
│   ├── Core_Windows.py            
│   ├── Digimon_Up_Main.py         
│   ├── Misc_Features.py           
│   ├── Emulator_Manager.py        # Gestor CLI de LDPlayer
│   ├── Digimon_Up_Script_M1.py    # Rutina completa desatendida
│   └── Digimon_Up_Script_M2.py    # Rutina corta de mantenimiento
├── res/                           
├── logs/                          
└── .gitignore                     
```

## Requisitos Previos

* **Sistema Operativo:** Windows 10 u 11 (64 bits).
* **Emulador:** LDPlayer con la instancia configurada con el nombre `"Boring Phone 14"`[cite: 7, 11].
* **Resolución del Emulador:** Configuración móvil vertical recomendada para coincidir con las plantillas visuales de la carpeta `res/`[cite: 7].
* **Python:** Versión 3.10 o superior.

---

## Instalación

1. **Clonar el repositorio:**
[https://github.com/littlejacket94/Digimon_Up_PyBot.git](https://github.com/littlejacket94/Digimon_Up_PyBot.git)
  ```bash
   git clone https://github.com/littlejacket94/Digimon_Up_PyBot.git
   cd Digimon_Up_PyBot
  ```
2. **Crear y activar un entorno virtual:**
  ```bash
     python -m venv venv
     # En Windows:
     venv\Scripts\activate
  ```
3. **Instalar las dependencias necesarias:**
  ```bash
     pip install opencv-python numpy pyautogui pygetwindow mss
  ```
4. **Verificar ruta de LDPlayer (solo para la rama** `cli`**)**  
Asegúrate de que la variable `LDCONSOLE_PATH` dentro de `app/Emulator_Manager.py` apunte a la ubicación real de tu archivo `ldconsole.exe`:  
   ```python
   LDCONSOLE_PATH = r"F:\LDPlayer\LDPlayer14\ldconsole.exe"
   ```

---

## Uso

### Rama `main` (Modo Directo)
Diseñada para correr el bot cuando el emulador ya está abierto y visible en pantalla.

```bash
git checkout main
python app/Digimon_Up_Main.py
```

### Rama `cli` (Modo Automatizado)
Diseñada para ejecución desatendida mediante el Programador de Tareas de Windows; abre el emulador vía línea de comandos, ejecuta la rutina seleccionada y cierra la instancia al finalizar.

```bash
git checkout cli

# Rutina completa (Fases 1 a 11):
python app/Digimon_Up_Script_M1.py

# Rutina rápida de mantenimiento (anuncios, recompensas y granja):
python app/Digimon_Up_Script_M2.py
```

---

## Explicación del Código

### Archivos Core
* **`app/Core_Windows.py`:** Administra las llamadas de la API de Windows y la visión artificial.
  * `obtener_rect_emulador()`: Detecta el identificador y tamaño de la ventana de LDPlayer.
  * `capturar_pantalla()`: Realiza la captura de pantalla rápida sobre la ventana mediante `mss`.
  * `buscar_coordenadas()`: Realiza el template matching utilizando `cv2.matchTemplate` bajo el método `TM_CCOEFF_NORMED`.
  * `clic()` / `deslizar()`: Convierte coordenadas relativas a la ventana en absolutas para simular eventos de ratón.
  * `cerrar_app()`: Abre el menú de aplicaciones recientes en LDPlayer (`F2`), arrastra la lista y pulsa el botón de borrado total (`BT.png`).

* **`app/Digimon_Up_Main.py`:** Contiene la lógica y los flujos de interacción dentro del juego.
  * `iniciar_app()`: Perro guardián (*watchdog*) con reintentos para mitigar congelamientos en pantallas de carga o cierres intempestivos al escritorio de Android (`SA.png`).
  * Funciones de mecánicas: `anuncios()`, `recompensas()`, `granja_de_carne()`, `calabozos()`, `sorteos()`, `jcj()`, `gemas_diarias()` y `ciclo_idle()`.

* **`app/Misc_Features.py`:** Módulo auxiliar de interfaz y registro.
  * `animar_espera()`: Formatea la terminal mostrando ciclos de espera dinámicos sin saturar el búfer de texto.
  * `LoggerDoble` / `iniciar_logger()`: Duplica cualquier salida de `sys.stdout` y `sys.stderr` en un archivo con formato `.log` dentro de la carpeta `/logs`.

### Archivos CLI
* **`app/Emulator_Manager.py`:** Interfaz con la consola de comandos de LDPlayer (`ldconsole.exe`)[cite: 1].
  * `iniciar_emulador()` / `cerrar_emulador()`: Inicia o apaga la máquina virtual en frío.
  * `posicionar_emulador_a_la_izquierda()`: Ancla la ventana a las coordenadas `(0, 0)` para mantenerla alejada de notificaciones o popups emergentes de Windows.
  * `esperar_emulador_listo()`: Supervisa el arranque de Android enviando pulsaciones reactivas de `Esc` para remover anuncios emergentes internos.
* **`app/Digimon_Up_Script_M1.py` y `app/Digimon_Up_Script_M2.py`:** Scripts de orquestación diseñados para ejecutarse sin supervisión en horarios automatizados.

---

## Historial de Versiones
### BASE
* **`v0.5`**: Versión preliminar funcional con arquitectura monolítica, comprobaciones básicas de plantillas y ejecución secuencial directa.
* **`v0.5.1`**: Optimización de `intervalo_entre_clics` en `esperar_y_clicar` (reducido de 2.0s a 1.0s) y conversión de `img_confirmacion` de constante fija a parámetro dinámico en funciones de calabozos.
* **`v1.0`**: Modularización del motor desacoplado en `Core_Windows.py`, `Digimon_Up_Main.py` y `Misc_Features.py`; incorporación del perro guardián (*watchdog*) en `iniciar_app()` contra bloqueos de carga, función `cerrar_app()` y sistema de logging dual en archivo.  
* **`v1.0.1`**: Se cambio el directorio `logs` a la raiz del proyecto en lugar de la carpeta `app\` se agrego la `Granja 4` a las granjas de carne.   
* **`v1.0.2-cli`**: Se cambio la funcion de `clic()` en `ciclo_calabozo()` por `esperar_clic_y_confirmar()` en la interaccion con las variables `img_tarjeta_calabozo` y `img_bttn_intentar` para mejorar la precision de los clics en calabozos. Se cambio la funcion `ciclo_idle` agregando un segundo parametro a `imgs_bttn_vender` y un ciclo for para verificar entre las dos o mas imagenes. reparar logs basura.
### CLI  
* **`v1.0-cli`**: Creación de la rama CLI con soporte para `Emulator_Manager.py` vía `ldconsole.exe`, separación de rutinas en scripts `Digimon_Up_Script_M1.py` y `Digimon_Up_Script_M2.py`, y reubicación automática de la ventana a coordenadas `(0, 0)`.
* **`v1.0.1-cli`**: Bucle reactivo con pulsaciones periódicas de la tecla `Esc` en `esperar_emulador_listo()` para eludir anuncios internos de LDPlayer, eliminación de funciones redundantes (`limpiar_anuncios_emulador`) y corrección del nombre del archivo de registro en el script `M2`.
* **`v1.0.2-cli`**: Union de la rama v1.0.1 base a cli, reparacion menor en la funcion `esperar_emulador_listo()` para revisar anuncios incluso si ya se encontro la imagen de confirmacion de arranque `SA.png`