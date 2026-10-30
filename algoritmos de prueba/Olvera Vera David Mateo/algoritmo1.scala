/* Algoritmo de prueba - Comentario de varias lineas */
def calcularArea(base: Float, altura: Float): Float = {
  val resultado: Float = base * altura // comentario de una linea
  return resultado
}

var contador: Int = 0;
val limite: Int = 5
val notas: Array[Float] = Array(8.5f, 9.0f, 7.2f)
val materias: List[String] = List("POO", "LP", "SO")

while (contador < limite) {
  if (contador % 2 == 0) {
    println("par")
  } else if (contador == 3) {
    println("tres")
  } else {
    println("impar")
  }
  contador += 1
}

for (i <- 1 to 3) {
  println(i * 2)
}

val area: Float = calcularArea(2.5f, 4.0f)
val activo: Boolean = true && !false