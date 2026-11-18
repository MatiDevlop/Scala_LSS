// =========================================================================
// ALGORITMO DE SUSTENTACIÓN - CASOS INCORRECTOS (ERRORES INTENCIONALES)
// =========================================================================

// --- 1. ANALIZADOR LÉXICO (Caracteres y símbolos fuera del alfabeto) ---
var @#variable_Incorrecta = 14
val simboloInvalido = "Error léxico"¿


// --- 2. ANALIZADOR SINTÁCTICO (Errores de estructura gramatical) ---
// Variables y tipos no reconocidos
var tipo_incorrecto1: Unit = 247
var tipo_incorrecto2: Byte = 247
var tipo_incorrecto3: Long = 247
var tipo_incorrecto4: Double = 247.78
var tipo_incorrecto5: Short = 247
val mapaInvalido: Map[String, Int] = Map("Ana" -> 30, "Carlos" -> 25)
val vectorInvalido: Vector[Int] = Vector(1, 2, 3, 4, 5)
val sinAsignacion: Int 20
var tipoNoSoportado: Integer = 30

// Operadores no soportados y expresiones mal formadas
var potencia = 2 ** 7
var acumuladoErr: Float = 100.5f
acumuladoErr += 20.4
acumuladoErr %= 2
acumuladoErr **= 2
var parentesisIncompleto: Int = (15 - 3 * 2
var exprMalFormada: Int = 10 + * 5

// Expresiones lógicas y relacionales inválidas
var mayor_edad = true
var es_ecuatoriano = false
var puede_ser_presidente2 = mayor_edad and es_ecuatoriano
var hacer_compras2 = mayor_edad or es_ecuatoriano
var puede_hablar_ingles2 = not es_ecuatoriano
var es_muy_mayor_a_2 = 10 >> 2
val condicionRota: Boolean = 10 > && true

// Estructuras de control mal formadas
if 10 == 10 {
  println("Faltan paréntesis")
}

for (step 1 to 4) {
  println(step)
}

// Estructura de datos Array con delimitadores erróneos
val arregloInvalido: Array{Int} = Array(1, 2, 3)

// Funciones sin tipo de parámetro o sin '='
def funcionSinTipo(a, b): Int = {
  return a + b
}

def funcionSinIgual(a: Int): Int {
  a + 10
}


// --- 3. ANALIZADOR SEMÁNTICO (Inconsistencias de tipos, ámbitos e identificadores) ---
// Declaraciones base para probar errores semánticos
var contadorSem: Int = 10
val constanteSem: String = "Inmutable"
var enteroSem: Int = 40

// Error: Uso de variable no declarada previamente
println(variableFantasma + 5)

// Error: Variable declarada dos veces en el mismo ámbito
var contadorSem: Int = 99

// Error: Reasignación de una constante ('val')
constanteSem = "Intento de cambio"

// Error: Conversión implícita inválida de Float a Int
var enteroConFloat: Int = 18.75f

// Error: Función declara retornar Int pero retorna String
def retornoIncompatible(n: Int): Int = {
  return "Texto en lugar de entero"
}

// Error: Operación aritmética inválida entre String y Boolean
var restaInvalida = "Hola" - true

// Error: Condición de estructura 'if' que no evalúa a Boolean (es Int)
if (enteroSem) {
  println("Condición no booleana")
}