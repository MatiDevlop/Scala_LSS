import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from lexic_analyzer import lexer
import syntactic_analyzer

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

    ruta_archivo_scala = os.path.join(ruta_carpeta_integrante, nombre_archivo)

    if not os.path.exists(ruta_archivo_scala):
        print(f"\n[ERROR] El archivo '{nombre_archivo}' no existe en la ruta: {ruta_archivo_scala}")
        print("Cerrando el programa...")
        sys.exit(1)

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    with open(ruta_archivo_scala, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    nombre_base = os.path.splitext(os.path.basename(nombre_archivo))[0]
    timestamp = datetime.now(ZONA_ECUADOR).strftime("%Y-%m-%d_%H-%M-%S")
    
    nombre_archivo_log = f"sintactico-{nombre_base}-{nombre_log_integrante}-{timestamp}.txt"
    archivo_log_salida = os.path.join(CARPETA_SALIDA, nombre_archivo_log)

    print(f"\nProcesando '{ruta_archivo_scala}'...")
    print(f"Guardando reporte en '{archivo_log_salida}'...\n")

    # Limpiar estados previos antes de parsear
    lexer.lineno = 1
    syntactic_analyzer.errores_sintacticos.clear()
    syntactic_analyzer.errores_semanticos.clear()
    syntactic_analyzer.tabla_simbolos["variables"].clear()
    syntactic_analyzer.variables_ocultas.clear()

    # Ejecutar el análisis sintáctico
    codigo_completo = "".join(lineas)
    syntactic_analyzer.parser.parse(codigo_completo, lexer=lexer)

    errores = syntactic_analyzer.errores_sintacticos

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
        if not errores:
            log_file.write("ESTADO: ÉXITO (0 Errores Sintácticos)\n")
            log_file.write("El código analizado cumple con todas las reglas gramaticales definidas.\n")
        else:
            log_file.write(f"ESTADO: FALLO ({len(errores)} Errores Encontrados)\n\n")
            for err in errores:
                log_file.write(f" [ERROR] {err}\n")

        log_file.write("\n==================================================\n")

    print("=== ANÁLISIS FINALIZADO ===")
    if not errores:
        print("✔ El código es sintácticamente VÁLIDO.")
    else:
        print(f"✖ Se encontraron {len(errores)} errores sintácticos.")
    print(f"Reporte generado en: {archivo_log_salida}")

if __name__ == '__main__':
    main()