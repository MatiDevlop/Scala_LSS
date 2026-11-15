// =========================================================================
// PRUEBA DE ANÁLISIS SEMÁNTICO - SCALA
// =========================================================================

// -------------------------------------------------------------------------
// SECCIÓN 1: CASOS VÁLIDOS (Deben pasar sin generar errores)
// -------------------------------------------------------------------------

// 1. Declaraciones válidas (tipadas e inferidas, val y var)
val tasaImpuesto: Float = 0.15f
var subtotal = 100
var totalPagar: Float = 0.0f
val moneda: String = "USD"
val esClienteFrecuente = true

// 2. Operaciones aritméticas compatibles (Int y Float)
val descuento = 10 * 2
totalPagar = subtotal + (subtotal * tasaImpuesto) - descuento

// 3. Concatenación válida con '+' (al menos un operando es String)
val mensajeFactura = "Total a pagar: " + totalPagar + " " + moneda
val resumenItems = subtotal + " articulos procesados"

// 4. Reasignaciones y asignaciones compuestas válidas sobre variables 'var'
subtotal = 150
subtotal += 25
totalPagar *= 1.05f

// 5. Estructuras de control y funciones tipadas válidas
def calcularEnvio(peso: Int): Float = {
    val tarifaBase: Float = 5.5f
    return peso * tarifaBase
}

if (subtotal > 100 && esClienteFrecuente) {
    println(mensajeFactura)
}

/*
// -------------------------------------------------------------------------
// SECCIÓN 2: ERRORES SEMÁNTICOS INDUCIDOS (Deben ser detectados)
// -------------------------------------------------------------------------

// ERROR 1 (Regla 1 - Tabla 14): Redeclaración de identificador existente
val tasaImpuesto: Float = 0.12f
var subtotal = 200

// ERROR 2 (Regla 1 - Tabla 14): Uso de identificador no declarado
val calculoInvalido = variableFantasma + 50
otroIdentificadorInexistente = 10
println(datoNoDefinido)

// ERROR 3 (Regla 2 - Tabla 15): Reasignación simple sobre constante 'val'
tasaImpuesto = 0.20f
moneda = "EUR"

// ERROR 4 (Regla 2 - Tabla 15): Asignación compuesta sobre constante 'val'
descuento += 5
tasaImpuesto *= 2

// ERROR 5 (Regla 3 - Tabla 16): Operaciones aritméticas con tipos incompatibles
val errorMultiplicacion = "Juan" * 5
val errorResta = moneda - 10
val errorDivision = esClienteFrecuente / 2
val errorModulo = "Texto" % 3
val errorSumaBool = true + 15
*/