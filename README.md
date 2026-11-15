<div align="center">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDcNUHg0yx8QzbBV8HU1rVnKlrjCYmda5lRojlbvb8iQ&s" alt="Logo de Scala" width="220" />
  <h1>Scala_LSS</h1>
  <p><strong>Analizador Léxico, Sintáctico y Semántico para el lenguaje Scala</strong></p>
</div>

---

## 📋 Descripción

**Scala_LSS** es una herramienta desarrollada en Python que permite realizar el análisis **léxico, sintáctico y semántico** de código fuente escrito en Scala. El proyecto cuenta con una interfaz gráfica de usuario (GUI) intuitiva y scripts de prueba en consola que generan archivos de registro (`.txt`) detallados.

---

## 📁 Estructura del Proyecto

```text
Scala_LSS/
│
├── algoritmos de prueba/                     # Carpeta con los archivos de prueba (.scala)
│   ├── Morocho Sani Kevin Matías/
│   └── Olvera Vera David Mateo/
│
├── logs/                           # Registros (.txt) generados tras cada análisis
├── app.py                          # Archivo principal de la Interfaz Gráfica (GUI)
├── test_lexer.py                   # Script de prueba para el analizador léxico
├── test_parser.py                  # Script de prueba para el analizador sintáctico
├── test_semantic.py                # Script de prueba para el analizador semántico
├── lexic_analyzer.py               # Lógica del analizador léxico (lexer)
├── syntactic_analyzer.py           # Lógica del analizador sintáctico (parser) y semántico (tabla de símbolos)
├── requerimientos.txt              # Dependencias del proyecto
└── README.md                       # Documentación del proyecto
```

---

## 🖥️ Ejecución mediante Interfaz Gráfica (GUI)

Para facilitar la interacción con el programa, se recomienda utilizar **PyCharm** y seguir estos pasos:

### 1. Instalación de dependencias
Abre la terminal integrada en PyCharm y ejecuta el siguiente comando para instalar las librerías necesarias:

```bash
pip install -r requerimientos.txt
```

### 2. Iniciar la aplicación
1. Abre el archivo **`app.py`** en el editor.
2. Haz clic en el **botón de ejecución (`▶ Run`)** en la esquina superior derecha de PyCharm.
3. *(Opcional)* También puedes iniciar la interfaz directamente desde la terminal ejecutando:
   ```bash
   python app.py
   ```

---

## 🧪 Pruebas en Consola (Sin Interfaz Gráfica)

Si prefieres probar cada fase del compilador de manera independiente desde la terminal, ejecuta el comando correspondiente. Cada ejecución generará automáticamente un archivo de registro (`.txt`).

| Fase del Analizador | Archivo | Comando de Ejecución |
| :--- | :--- | :--- |
| **Analizador Léxico** | `test_lexer.py` | `python test_lexer.py` |
| **Analizador Sintáctico** | `test_parser.py` | `python test_parser.py` |
| **Analizador Semántico** | `test_semantic.py` | `python test_semantic.py` |

---

## ⚙️ Flujo de Ejecución en Consola

Al iniciar cualquiera de los scripts de prueba anteriores, la consola te solicitará de manera interactiva los siguientes tres datos:

1. **Nombre de la carpeta del algoritmo:**  
   Selecciona el directorio correspondiente al autor del algoritmo:
   * `Morocho Sani Kevin Matías`
   * `Olvera Vera David Mateo`

2. **Responsable del log:**  
   Escribe el nombre de la persona encargada de generar o revisar el archivo de registro.

3. **Nombre del algoritmo a ejecutar (sin extensión):**  
   Ingresa el nombre del archivo de prueba ubicado dentro de la carpeta seleccionada previamente.

---

## 👥 Autores

* **Morocho Sani Kevin Matías**
* **Olvera Vera David Mateo**
