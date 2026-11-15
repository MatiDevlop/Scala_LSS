import os
from datetime import datetime
from zoneinfo import ZoneInfo
from lexic_analyzer import lexer, lista_errores
from syntactic_analyzer import (
    parser,
    tabla_simbolos,
    variables_ocultas,
    errores_sintacticos,
    errores_semanticos,
)

def ejecutar_prueba_semantica(carpeta_integrante, responsable, nombre_algoritmo):
    # 1. Construir la ruta exacta dentro de "algoritmos de prueba"
    ruta_archivo = os.path.join("algoritmos de prueba", carpeta_integrante, f"{nombre_algoritmo}.scala")

    if not os.path.exists(ruta_archivo):
        print(f"\n[ERROR] No se encontró el archivo en la ruta: '{ruta_archivo}'")
        return

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        codigo_fuente = archivo.read()

    # 2. Reiniciar estado completo del lexer, parser, tabla de símbolos y listas de errores
    lexer.lineno = 1
    lista_errores.clear()
    tabla_simbolos["variables"].clear()
    variables_ocultas.clear()
    errores_sintacticos.clear()
    errores_semanticos.clear()

    # 3. Ejecutar el análisis sintáctico y semántico
    parser.parse(codigo_fuente, lexer=lexer)

    # 4. Obtener fecha y hora actual en Guayaquil, Ecuador
    zona_ecuador = ZoneInfo("America/Guayaquil")
    ahora_ecuador = datetime.now(zona_ecuador)
    fecha_str = ahora_ecuador.strftime("%Y-%m-%d")
    hora_str = ahora_ecuador.strftime("%H-%M-%S")
    fecha_hora_completa = f"{fecha_str}_{hora_str}"

    # 5. Evaluar resultados semánticos
    total_errores = len(errores_semanticos)
    estado = "ÉXITO (0 Errores)" if total_errores == 0 else f"FALLO ({total_errores} Errores Encontrados)"

    lineas_reporte = [
        "=" * 55,
        "          REPORTE DEL ANALIZADOR SEMÁNTICO             ",
        "=" * 55,
        f"Responsable del Log       : {responsable}",
        f"Carpeta del Integrante    : {carpeta_integrante}",
        f"Archivo Analizado         : {nombre_algoritmo}.scala",
        f"Fecha y Hora (Guayaquil)  : {fecha_str} {ahora_ecuador.strftime('%H:%M:%S')}",
        "=" * 55,
        "",
        "--- CÓDIGO FUENTE EVALUADO ---"
    ]

    for idx, linea in enumerate(codigo_fuente.splitlines(), start=1):
        lineas_reporte.append(f"{idx:03d} | {linea}")

    lineas_reporte.extend([
        "=" * 55,
        "",
        "--- RESULTADO DEL ANÁLISIS SEMÁNTICO ---",
        f"ESTADO: {estado}",
        ""
    ])

    if total_errores > 0:
        for err in errores_semanticos:
            lineas_reporte.append(f" [ERROR] {err}")
    else:
        lineas_reporte.append(" No se detectaron errores semánticos.")

    lineas_reporte.extend([
        "",
        "=" * 55
    ])

    contenido_final = "\n".join(lineas_reporte)

    # 6. Guardar en la carpeta "logs" con el formato exacto solicitado
    carpeta_salida = "logs"
    os.makedirs(carpeta_salida, exist_ok=True)
    
    nombre_log = f"semantico-{nombre_algoritmo}-{responsable}-{fecha_hora_completa}.txt"
    ruta_log = os.path.join(carpeta_salida, nombre_log)

    with open(ruta_log, "w", encoding="utf-8") as log_file:
        log_file.write(contenido_final)

    print(f"\nLog generado exitosamente en: {ruta_log}")
    print(f"Resultado: {estado}")


if __name__ == "__main__":
    print("=" * 55)
    print("      GENERADOR DE LOGS - ANALIZADOR SEMÁNTICO")
    print("=" * 55)

    # 1. Preguntar por la carpeta dentro de "algoritmos de prueba"
    carpeta_integrante = input("Nombre de la carpeta en 'algoritmos de prueba' (ej. Morocho Sani Kevin Matías): ").strip()
    
    # 2. Preguntar por el responsable del log
    responsable = input("Responsable del log (ej. KevinMorocho): ").strip()
    
    # 3. Preguntar por el nombre del archivo sin extensión
    nombre_algoritmo = input("Nombre del algoritmo (sin extensión .scala, ej. algoritmo3): ").strip()
    
    # Limpieza preventiva si el usuario incluye la extensión
    if nombre_algoritmo.endswith(".scala"):
        nombre_algoritmo = nombre_algoritmo[:-6]

    ejecutar_prueba_semantica(
        carpeta_integrante=carpeta_integrante,
        responsable=responsable,
        nombre_algoritmo=nombre_algoritmo
    )