// =========================================================================
// SECCIÓN 1: CUMPLE REGLAS (Código válido en las 3 fases)
// =========================================================================


val piFloat: Float = 3.141592F
var contadorEntero: Int = 0
val mensaje: String = "Inicia el procesamiento..."
var acumulado: Float = 100.5f
acumulado += 20.4
acumulado -= 2
acumulado *= 2
acumulado /= 2
var operacion_modulo: Int = 17 % 4
contadorEntero += 1
val esValido: Boolean = (contadorEntero > 0 && acumulado >= 50.0F) || false
val estadoAlerta: Boolean = !(acumulado == 0) && (contadorEntero <= 5.0f)
val verificacionExacta: Boolean = (acumulado != 0.0f) || (contadorEntero < 10)
val tasaAprobacion: Float = 7.5f
var contadorValido: Int = 0
val mensajeInicio: String = "Iniciando evaluación de sustentación..."
var esActivo: Boolean = true

val calificaciones: Array[Int] = Array(8, 9, 6, 10)
var edad = 18
val año = 2026
var nombre: String = "Messi Ronaldo"
val dinero: Float = 7.8F

def calcularPromedio(nota1: Float, nota2: Float): Float = {
  val sumaNotas: Float = nota1 + nota2
  return sumaNotas / 2.0f
}

for (i <- 1 to 3) {
    println(i * 10)
}

def verificarBeca(puntaje: Float): Boolean = {
  val sumaNotas: Float = puntaje + 0.5f
  sumaNotas >= tasaAprobacion
}



// =========================================================================
// SECCIÓN 2: NO CUMPLE REGLAS (Errores intencionales controlados)
// =========================================================================

// --- 2.1 Subsección Léxica (Caracteres no reconocidos en el alfabeto de Scala) ---
var datoCorrupto: Int = 45?90
val simboloInvalido: String = "Error léxico"¿

// --- 2.2 Subsección Sintáctica (Errores de estructura gramatical y tokens) ---
var tipoMalEscrito: Integer = 100
val expresionIncompleta: Int = (10 + 5

// --- 2.3 Subsección Semántica (Inmutabilidad, tipos, duplicados y no declaradas) ---
// Error 1: Reasignación de variable inmutable ('val')
tasaAprobacion = 8.0f

// Error 2: Conversión implícita inválida de Float a Int
var enteroInvalido: Int = 12.75f

// Error 3: Variable declarada dos veces en el mismo ámbito
var contadorValido: Int = 5

// Error 4: Uso de variable no declarada previamente
println(variableInexistente + 10)

// Error 5: Condición de estructura 'if' que no es Boolean
if (contadorValido) {
  println("Condición inválida")
}