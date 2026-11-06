import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from lexic_analyzer import lexer, lista_errores

# Evitar la creación de carpetas __pycache__
sys.dont_write_bytecode = True

CARPETA_BASE = "algoritmos de prueba"
CARPETA_LOGS = "logs"
ZONA_ECUADOR = ZoneInfo("America/Guayaquil")


def analizar_y_generar_log(ruta_archivo: str, nombre_responsable: str):
    nombre_archivo = os.path.basename(ruta_archivo)
    nombre_sin_ext, _ = os.path.splitext(nombre_archivo)

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    lexer.input(codigo)
    lexer.lineno = 1
    lista_errores.clear()

    tokens_encontrados = []
    for tok in lexer:
        tokens_encontrados.append(tok)

    # Identificador sin espacios para el nombre físico del archivo .txt
    identificador_archivo = "".join(nombre_responsable.split())
    marca_tiempo = datetime.now(ZONA_ECUADOR).strftime("%d-%m-%Y-%Hh%M")
    
    # Nombre del archivo: lexico-NombreArchivo-NombreResponsable-DD-MM-YYYY-HHhMM.txt
    nombre_log = f"lexico-{nombre_sin_ext}-{identificador_archivo}-{marca_tiempo}.txt"
    ruta_log = os.path.join(CARPETA_LOGS, nombre_log)

    os.makedirs(CARPETA_LOGS, exist_ok=True)

    with open(ruta_log, "w", encoding="utf-8") as out:
        out.write("======================================================================\n")
        out.write("                    REPORTE DE ANÁLISIS LÉXICO                        \n")
        out.write("======================================================================\n")
        out.write(f"Archivo analizado : {nombre_archivo}\n")
        out.write(f"Ruta fuente       : {ruta_archivo}\n")
        out.write(f"Responsable       : {nombre_responsable}\n")
        out.write(f"Fecha y hora      : {datetime.now(ZONA_ECUADOR).strftime('%d/%m/%Y %H:%M:%S')}\n")
        out.write("======================================================================\n\n")

        # 1. Tabla de tokens reconocidos
        out.write(f"{'LÍNEA':<8}{'TIPO DE TOKEN':<25}{'LEXEMA'}\n")
        out.write("-" * 70 + "\n")
        for tok in tokens_encontrados:
            out.write(f"{tok.lineno:<8}{tok.type:<25}{str(tok.value)}\n")

        # 2. Resumen de errores léxicos
        out.write("\n" + "=" * 70 + "\n")
        out.write("REGISTRO DE ERRORES LÉXICOS\n")
        out.write("=" * 70 + "\n")
        if lista_errores:
            out.write(f"Total de errores detectados: {len(lista_errores)}\n\n")
            for err in lista_errores:
                out.write(f"[ERROR LÉXICO] {err}\n")
        else:
            out.write("No se detectaron errores léxicos. Todos los tokens fueron clasificados con éxito.\n")

    print(f"\n[✓] Log generado correctamente en: {ruta_log}")


def main():
    print("=" * 60)
    print("        SISTEMA DE PRUEBAS DEL ANALIZADOR LÉXICO (SCALA)      ")
    print("=" * 60)

    # 1. Nombre de la carpeta física donde reside el archivo
    nombre_carpeta = input("Ingrese el nombre exacto de la carpeta del integrante: ").strip()
    ruta_carpeta_integrante = os.path.join(CARPETA_BASE, nombre_carpeta)

    if not os.path.isdir(ruta_carpeta_integrante):
        print(f"\n[ERROR] No existe la carpeta '{nombre_carpeta}' dentro de '{CARPETA_BASE}'.")
        print(f"Ruta buscada: {ruta_carpeta_integrante}")
        return

    # 2. Nombre que debe aparecer en el reporte y en el archivo .txt
    nombre_log_integrante = input("Ingrese el nombre/apellido que aparecerá en el log (ej. KevinMorocho): ").strip()
    if not nombre_log_integrante:
        print("\n[ERROR] El nombre para el log no puede estar vacío.")
        return

    # 3. Nombre del archivo a evaluar
    nombre_archivo = input("Ingrese el nombre del archivo a probar (ej. algoritmo1): ").strip()
    if not nombre_archivo.endswith(".scala"):
        nombre_archivo += ".scala"

    ruta_archivo_scala = os.path.join(ruta_carpeta_integrante, nombre_archivo)

    if not os.path.isfile(ruta_archivo_scala):
        print(f"\n[ERROR] No se encontró el archivo '{nombre_archivo}' en la carpeta '{nombre_carpeta}'.")
        print(f"Ruta buscada: {ruta_archivo_scala}")
        return

    # 4. Ejecución del análisis
    print(f"\nProcesando '{nombre_archivo}'...")
    analizar_y_generar_log(ruta_archivo_scala, nombre_log_integrante)


if __name__ == "__main__":
    main()