
// FINAL - DAVID OLVERA -  (0 errores)


// ------------------------------ COMENTARIOS -----------------------------
// Comentario de una linea
/* Comentario de
   varias lineas */

// ------------------------------ ESTRUCTURAS DE DATOS --------------------
val numeros: List[Int] = List(1, 2, 3)
val nombres: List[String] = List("Ana", "Luis")
val vacia = List()
val notas: Array[Float] = Array(8.5f, 9.0f, 7.2f)

// ------------------------------ PRINTLN / PRINT -------------------------
println("Hola")
println()
print("Sin salto")

// ------------------------------ ENTRADA POR TECLADO ---------------------
val texto: String = readLine()
val edad: Int = readInt()
val linea = scala.io.StdIn.readLine()
val edadUsuario: Int = scala.io.StdIn.readInt()

// ------------------------------ CONVERSION ------------------------------
val precio: Float = 10
val ratio: Float = 2.5f

// ------------------------------ FUNCIONES -------------------------------
def suma(a: Int, b: Int): Int = {
  return a + b
}

def promedio(x: Float, y: Float): Float = {
  return (x + y) / 2.0f
}

def doble(n: Int): Int = n * 2

def uno(): Int = 1

def esNumeroPar(numero: Int): Boolean = (numero % 2) == 0

val resultado = suma(2, 3)
val d = doble(4)
println(suma(1, 2))

// ------------------------------ FUNCIONES ANONIMAS ----------------------
val triple = (x: Int) => x * 3
val multiplicar = (x: Int, y: Int) => x * y

// ------------------------------ IF / ELSE IF / ELSE ---------------------
var contador: Int = 0
val limite: Int = 5

if (contador < limite) {
  println("menor")
} else if (contador == limite) {
  println("igual")
} else {
  println("mayor")
}

// ------------------------------ WHILE -----------------------------------
while (contador < limite) {
  contador += 1
}

// ------------------------------ FOR -------------------------------------
for (i <- 1 to 3) {
  println(i * 10)
}