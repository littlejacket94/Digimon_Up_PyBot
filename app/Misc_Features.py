import sys
import os
from datetime import datetime

# Variables Globales
_contador_animacion = 0

# Clase LoggerDoble
class LoggerDoble:
    """Redirige prints y errores simultáneamente a consola y archivo .log."""
    def __init__(self, prefijo="bot"):
        self.terminal = sys.stdout
        
        # Guardar en la subcarpeta /logs dentro de la raíz del proyecto
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.logs_dir = os.path.join(base_dir, "logs")
        os.makedirs(self.logs_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_path = os.path.join(self.logs_dir, f"{prefijo}_{timestamp}.log")
        self.log_file = open(self.log_path, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)
        self.log_file.flush()

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

# Funciones Misc
def animar_espera(mensaje="Esperando"):
    """Muestra una animación cíclica de puntos en la misma línea."""
    global _contador_animacion
    puntos = ["", " .", " . .", " . . ."]
    estado = puntos[_contador_animacion % len(puntos)]
    _contador_animacion += 1
    
    # \r regresa al inicio de la línea y ljust(25) borra el texto sobrante anterior
    sys.stdout.write(f"\r{mensaje}{estado}".ljust(25))
    sys.stdout.flush()

def limpiar_linea_espera():
    """Limpia la línea de la animación para que el siguiente print salga limpio."""
    sys.stdout.write("\r" + " " * 25 + "\r")
    sys.stdout.flush()

def iniciar_logger(prefijo="ejecucion"):
    """Activa la captura completa de salidas en consola y excepciones."""
    logger = LoggerDoble(prefijo=prefijo)
    sys.stdout = logger
    sys.stderr = logger
    print(f"=== Registro iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    return logger