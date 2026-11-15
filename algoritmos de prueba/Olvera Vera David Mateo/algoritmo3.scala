// Algoritmo 3 - Pruebas semanticas 

// ---------- Parte valida ----------
var contador: Int = 0
val limite: Float = 10
val promedio: Float = 7
var activo: Boolean = true

def sumar(a: Int, b: Int): Int = {
  val total = a + b
  return total
}

def obtenerNota(a: Int): Float = {
  return a
}

if (contador < 5) {
  println("menor")
} else if (activo) {
  println("activo")
}

while (contador < 3) {
  contador = contador + 1
}

// ---------- Errores  ----------
// Conversion
val valorEntero: Int = 12.85F

// Estructuras de control
while (contador) {
  println("ciclo")
}

if (activo == true) {
  println("ok")
} else if (limite) {
  println("error")
}

// Retorno de funciones
def obtenerPromedio(a: Float, b: Float): Float = {
  val suma = a + b
  return "Resultado " + suma
}