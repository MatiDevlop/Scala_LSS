// Algoritmo 4 - Prueba general del proyecto
// Parte valida y errores lexicos, semanticos y sintactico

// ---------- Parte valida ----------
val tasaImpuesto: Float = 0.15f
var subtotal = 100
var contador: Int = 0
val numeros: List[Int] = List(1, 2, 3)

def calcularEnvio(peso: Int): Float = {
  val tarifa: Float = 5.5f
  return peso * tarifa
}

for (i <- 1 to 3) {
  println(i)
}

if (subtotal > 50) {
  println("compra grande")
} else if (contador == 0) {
  println("sin compras")
}

while (contador < 3) {
  contador = contador + 1
}

// ---------- Errores lexicos ----------
val usuario = "Ana" @
var codigo = 10 #

// ---------- Errores semanticos ----------
val calculo = variableFantasma + 50
tasaImpuesto = 0.20f
val valorEntero: Int = 12.85F
def obtenerPromedio(a: Float, b: Float): Float = {
  val suma = a + b
  return "Resultado " + suma
}

// ---------- Error sintactico ----------
val resultado = = 5