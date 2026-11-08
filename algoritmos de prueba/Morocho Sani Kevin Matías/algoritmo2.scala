// --- Declaración e Inicialización de Variables y Listas ---
val limiteAprobacion: Int = 60
var contadorAprobados: Int = 0
var sumaTotalNotas: Float = 0.0f
var notaActual: Int = 0

// Lista de IDs de estudiantes
val listaEstudiantes: List[Int] = List(1, 2, 3, 4, 5)

// --- Definición de una función auxiliar ---
def mostrarMensaje(mensaje: String): String = mensaje

// --- Bucle para procesar la lista de estudiantes ---
for (estudianteId <- 1 to 5) {
    // Ingresar datos por teclado para simular o actualizar la nota actual
    print("Ingrese la nota actual para el estudiante: ")
    notaActual = readInt()

    // Evaluamos el estado del estudiante mediante una Estructura Condicional (If / Else)
    if (notaActual >= limiteAprobacion) {
        println("Estudiante Aprobado")
        contadorAprobados += 1
    } else {
        println("Estudiante Reprobado")
    }

    // Acumulamos y actualizamos contadores mediante Asignación Compuesta
    sumaTotalNotas += notaActual
}

// --- Bucle No Condicionado (For): Simulación de Reporte Final ---
for (i <- 1 to 3) {
    println(i * 10)
}

def sumarNumero(numeroA:Int, numeroB:Int):Int = {
    val resultado = numeroA + numeroB
    resultado
}

def calcularAreaRectangulo(base:Float, altura:Float):Float = {
    val resultado = base * altura
    return resultado
}