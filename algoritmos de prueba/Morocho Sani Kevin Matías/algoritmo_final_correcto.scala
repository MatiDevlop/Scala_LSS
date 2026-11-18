// =========================================================================
// ALGORITMO DE SUSTENTACIÓN - CASOS CORRECTOS (LÉXICO, SINTÁCTICO, SEMÁNTICO)
// =========================================================================

// --- 1. ANALIZADOR LÉXICO ---
// Variables
var variable1 = "Estoy aprendiendo Scala"
val constante1 = "Hola Mundo"

// Tipos de datos
var numero: Int = 123
var decimal: Float = 47.9F
var booleano: Boolean = true
var cadena: String = "Scala_LSS"
var caracter: Char = 'a'
val calificacionesArray: Array[Int] = Array(8, 9, 6, 10)
val calificacionesList: List[Int] = List(8, 9, 6, 10)

// Operadores aritméticos
var modulo = 17 % 4
var suma = 17 + 4
var resta = 17 - 4
var multiplicacion = 17 * 4
var division = 17 / 4

// Operadores de asignación
var acumulado: Float = 100.5f
acumulado += 20.4f
acumulado -= 2
acumulado *= 2
acumulado /= 2

// Operadores lógicos
var mayor_edad = true
var es_ecuatoriano = false
var puede_ser_presidente = mayor_edad && es_ecuatoriano
var hacer_compras = mayor_edad || es_ecuatoriano
var puede_hablar_ingles = !es_ecuatoriano

// Operadores relacionales
var contadorEntero: Int = 0
val esValido: Boolean = (contadorEntero > 0 && acumulado >= 50.0F) || false
val estadoAlerta: Boolean = !(acumulado == 0) && (contadorEntero <= 5.0f)
val verificacionExacta: Boolean = (acumulado != 0.0f) || (contadorEntero < 10)


// --- 2. ANALIZADOR SINTÁCTICO ---
// Declaración de variables
val limiteMax: Int = 50
var puntajeActual = 10

// Expresiones aritméticas
var calculoValido: Int = (10 + 5) * 2 - (8 / 4)

// Expresiones booleanas
val condicionValida: Boolean = (puntajeActual >= 5 && limiteMax != 0) || false

// Estructuras de control (condicional if/else, bucle while, bucle for)
if (puntajeActual < limiteMax) {
  puntajeActual += 5
} else {
  puntajeActual = 0
}

while (puntajeActual < 20) {
  puntajeActual += 2
}

for (step <- 1 to 4) {
  println(step)
}

// Estructura de datos (Array)
val arregloNotas: Array[Int] = Array(10, 9, 8, 7)

// Declaración de funciones (bloque con retorno explícito e implícito)
def sumarConReturnExplicito(a: Int, b: Int): Int = {
  val total: Int = a + b
  return total
}

def sumarConReturnImplicito(a: Int, b: Int): Int = {
  val total: Int = a + b
  total
}


// --- 3. ANALIZADOR SEMÁNTICO ---
// Identificadores (declaración, reasignación válida de 'var' e inmutabilidad de 'val')
var contadorSem: Int = 10
contadorSem = 25
val constanteSem: String = "Inmutable"

// Asignación de tipo compatible
var enteroSem: Int = 40
var flotanteSem: Float = 15.5f

// Operaciones permitidas (aritmética numérica, concatenación y condición Boolean)
var sumaNumerica: Float = enteroSem + flotanteSem
var concatenacionValida: String = "Resultado: " + enteroSem

if (enteroSem > 20 && constanteSem != "") {
  println(concatenacionValida)
}