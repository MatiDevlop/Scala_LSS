val lista: List[Int] = List(10, 20, 30)
def esPar(n: Int): Boolean = (n % 2) == 0
val multiplicar = (x: Int, y: Int) => x * y
val doble = (x: Int) => x * 2
val nombre: String = scala.io.StdIn.readLine()
val edad: Int = scala.io.StdIn.readInt()
println("Registro completado")
print(edad)
val par = esPar(edad)
if (edad >= 18 && !par) {
  println("mayor impar")
} else if (edad == 18 || edad < 5) {
  println("caso especial")
} else {
  println("otro")
}
val resultado = multiplicar(3, 4)
val letra: Char = 'a'