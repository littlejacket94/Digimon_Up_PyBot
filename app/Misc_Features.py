import sys

# Variables Globales
_contador_animacion = 0

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