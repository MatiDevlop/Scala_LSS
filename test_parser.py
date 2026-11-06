import os
import sys
from datetime import datetime
import ply.yacc as yacc
from lexic_analyzer import tokens
import syntactic_analyzer
from zoneinfo import ZoneInfo

# Definición de las carpetas según la estructura del proyecto
CARPETA_ENTRADA = "algoritmos de prueba"
CARPETA_SALIDA = "logs"
ZONA_ECUADOR = ZoneInfo("America/Guayaquil")

def main():
    print("=== SCRIPT DE PRUEBAS DEL ANALIZADOR SINTÁCTICO (SCALA) ===")
    
    # 1. Nombre de la carpeta física del integrante (ubicada dentro de 'algoritmos de prueba')
    nombre_carpeta = input("Ingrese el nombre exacto de la carpeta del integrante: ").strip()
    ruta_carpeta_integrante = os.path.join(CARPETA_ENTRADA, nombre_carpeta)

    if not os.path.isdir(ruta_carpeta_integrante):
        print(f"\n[ERROR] No existe la carpeta '{nombre_carpeta}' dentro de '{CARPETA_ENTRADA}'.")
        print(f"Ruta buscada: {ruta_carpeta_integrante}")
        sys.exit(1)

    # 2. Nombre que debe aparecer en el reporte y en el archivo de log
    nombre_log_integrante = input("Ingrese el nombre/apellido que aparecerá en el log (ej. KevinMorocho): ").strip()
    if not nombre_log_integrante:
        print("\n[ERROR] El nombre para el log no puede estar vacío.")
        sys.exit(1)

    # 3. Nombre del archivo a evaluar
    nombre_archivo = input("Ingrese el nombre del archivo a probar (ej. algoritmo1): ").strip()
    if not nombre_archivo.endswith(".scala"):
        nombre_archivo += ".scala"

    # Ruta completa del archivo .scala dentro de la carpeta del integrante
    ruta_archivo_scala = os.path.join(ruta_carpeta_integrante, nombre_archivo)

    # Validar existencia del archivo .scala
    if not os.path.exists(ruta_archivo_scala):
        print(f"\n[ERROR] El archivo '{nombre_archivo}' no existe en la ruta: {ruta_archivo_scala}")
        print("Cerrando el programa...")
        sys.exit(1)

    # Asegurar que la carpeta de salida 'logs' exista
    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    # Leer el contenido del archivo .scala
    with open(ruta_archivo_scala, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    nombre_base = os.path.splitext(os.path.basename(nombre_archivo))[0]
    
    # Generar la marca de tiempo actual (fecha y hora)
    timestamp = datetime.now(ZONA_ECUADOR).strftime("%Y-%m-%d_%H-%M-%S")
    
    # Construir el nombre del archivo de salida con la estructura solicitada: sintactico-<algoritmo>-<nombre>-<fecha>-<hora>.txt
    nombre_archivo_log = f"sintactico-{nombre_base}-{nombre_log_integrante}-{timestamp}.txt"
    archivo_log_salida = os.path.join(CARPETA_SALIDA, nombre_archivo_log)

    print(f"\nProcesando '{ruta_archivo_scala}'...")
    print(f"Guardando reporte en '{archivo_log_salida}'...\n")

    # Lista para recolectar errores durante el parsing
    errores_sintacticos = []

    # Redefinir la función de captura de errores para el log
    def custom_p_error(p):
        if p:
            msg = f"Error sintáctico en línea {p.lineno}: Token inesperado '{p.value}' (Tipo: {p.type})"
        else:
            msg = "Error sintáctico: Fin de archivo (EOF) inesperado"
        errores_sintacticos.append(msg)

    syntactic_analyzer.parser.errorfunc = custom_p_error

    # Analizar el código cargado
    codigo_completo = "".join(lineas)
    
    # Reiniciar contador de líneas del lexer si está disponible
    if hasattr(syntactic_analyzer, 'lexer'):
        syntactic_analyzer.lexer.lineno = 1

    resultado = syntactic_analyzer.parser.parse(codigo_completo)

    # Generar el reporte / log del Analizador Sintáctico en la carpeta 'logs'
    with open(archivo_log_salida, "w", encoding="utf-8") as log_file:
        log_file.write("==================================================\n")
        log_file.write("       REPORTE DEL ANALIZADOR SINTÁCTICO           \n")
        log_file.write("==================================================\n")
        log_file.write(f"Responsable del Algoritmo : {nombre_log_integrante}\n")
        log_file.write(f"Carpeta del Integrante    : {nombre_carpeta}\n")
        log_file.write(f"Archivo Analizado         : {nombre_archivo}\n")
        log_file.write(f"Fecha y Hora de Ejecución : {timestamp}\n")
        log_file.write("==================================================\n\n")

        log_file.write("--- CÓDIGO FUENTE EVALUADO ---\n")
        for num, linea in enumerate(lineas, 1):
            log_file.write(f"{num:03d} | {linea}")
        log_file.write("\n==================================================\n\n")

        log_file.write("--- RESULTADO DEL ANÁLISIS SINTÁCTICO ---\n")
        if not errores_sintacticos:
            log_file.write("ESTADO: ÉXITO (0 Errores Sintácticos)\n")
            log_file.write("El código analizado cumple con todas las reglas gramaticales definidas.\n")
        else:
            log_file.write(f"ESTADO: FALLO ({len(errores_sintacticos)} Errores Encontrados)\n\n")
            for err in errores_sintacticos:
                log_file.write(f" [ERROR] {err}\n")

        log_file.write("\n==================================================\n")

    # Resumen en consola
    print("=== ANÁLISIS FINALIZADO ===")
    if not errores_sintacticos:
        print("✔ El código es sintácticamente VÁLIDO.")
    else:
        print(f"✖ Se encontraron {len(errores_sintacticos)} errores sintácticos.")
    print(f"Reporte generado en: {archivo_log_salida}")

if __name__ == '__main__':
    main()