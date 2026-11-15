import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Importación del motor del compilador desarrollado por el grupo
import lexic_analyzer
import syntactic_analyzer


class InterfazCompiladorScala:
    def __init__(self, root):
        self.root = root
        self.root.title("Scala LSS Compiler IDE - Panel de Control")
        self.root.geometry("1250x720")
        self.root.minsize(1050, 620)

        self.responsable_var = tk.StringVar(value="KevinMorocho")
        self.nombre_algoritmo_actual = "workspace_gui"
        self.archivo_temporal = os.path.join("algoritmos de prueba", "workspace_gui.scala")

        self.crear_componentes()
        self.configurar_eventos()
        self.cargar_plantilla_inicial()

    def crear_componentes(self):
        # -----------------------------------------------------------------
        # 1. BARRA DE HERRAMIENTAS SUPERIOR (BOTONES DE ACCIÓN)
        # -----------------------------------------------------------------
        toolbar = ttk.Frame(self.root, padding=6)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open = ttk.Button(toolbar, text="Abrir Archivo (.scala)", command=self.abrir_archivo)
        btn_open.pack(side=tk.LEFT, padx=5)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        btn_lex = ttk.Button(toolbar, text="Analizar Léxico", command=self.ejecutar_lexico)
        btn_lex.pack(side=tk.LEFT, padx=5)

        btn_sin = ttk.Button(toolbar, text="Analizar Sintáctico", command=self.ejecutar_sintactico)
        btn_sin.pack(side=tk.LEFT, padx=5)

        btn_sem = ttk.Button(toolbar, text="Analizar Semántico", command=self.ejecutar_semantico)
        btn_sem.pack(side=tk.LEFT, padx=5)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        btn_all = ttk.Button(toolbar, text="COMPILAR TODO", style="Accent.TButton", command=self.compilar_todo)
        btn_all.pack(side=tk.LEFT, padx=5)

        # Selector de responsable del log a la derecha
        combo_resp = ttk.Combobox(
            toolbar,
            textvariable=self.responsable_var,
            values=["KevinMorocho", "DavidOlvera"],
            state="readonly",
            width=18
        )
        combo_resp.pack(side=tk.RIGHT, padx=5)
        ttk.Label(toolbar, text="Responsable Log:").pack(side=tk.RIGHT, padx=4)

        # -----------------------------------------------------------------
        # 2. PANEL PRINCIPAL DIVIDIDO (LADO A LADO)
        # -----------------------------------------------------------------
        panel_dividido = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        panel_dividido.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # --- LADO IZQUIERDO: EDITOR DE CÓDIGO SCALA ---
        frame_izquierdo = ttk.LabelFrame(panel_dividido, text=" Editor de Código Scala ", padding=5)
        panel_dividido.add(frame_izquierdo, weight=1)

        contenedor_editor = ttk.Frame(frame_izquierdo)
        contenedor_editor.pack(fill=tk.BOTH, expand=True)

        self.line_canvas = tk.Canvas(contenedor_editor, width=38, bg="#f0f0f0", bd=0, highlightthickness=0)
        self.line_canvas.pack(side=tk.LEFT, fill=tk.Y)

        scroll_y = ttk.Scrollbar(contenedor_editor)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_editor = tk.Text(
            contenedor_editor,
            wrap=tk.NONE,
            yscrollcommand=scroll_y.set,
            font=("Consolas", 11),
            undo=True,
            bg="#ffffff",
            fg="#000000",
            insertbackground="black"
        )
        self.txt_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.txt_editor.yview)

        scroll_x = ttk.Scrollbar(frame_izquierdo, orient=tk.HORIZONTAL, command=self.txt_editor.xview)
        self.txt_editor.config(xscrollcommand=scroll_x.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # --- LADO DERECHO: CENTRO DE DIAGNÓSTICO (LOGS) ---
        frame_derecho = ttk.LabelFrame(panel_dividido, text=" Diagnóstico y Reportes del Sistema ", padding=5)
        panel_dividido.add(frame_derecho, weight=1)

        self.notebook = ttk.Notebook(frame_derecho)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        config_consola = {
            "bg": "#1e1e1e",
            "fg": "#d4d4d4",
            "insertbackground": "white",
            "font": ("Consolas", 10),
            "wrap": tk.WORD
        }

        # Pestaña 1: Log Léxico
        self.tab_lexico = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_lexico, text=" Log Léxico ")
        self.txt_log_lexico = tk.Text(self.tab_lexico, **config_consola)
        self.txt_log_lexico.pack(fill=tk.BOTH, expand=True)

        # Pestaña 2: Log Sintáctico
        self.tab_sintactico = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sintactico, text=" Log Sintáctico ")
        self.txt_log_sintactico = tk.Text(self.tab_sintactico, **config_consola)
        self.txt_log_sintactico.pack(fill=tk.BOTH, expand=True)

        # Pestaña 3: Log Semántico
        self.tab_semantico = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_semantico, text=" Log Semántico ")
        self.txt_log_semantico = tk.Text(self.tab_semantico, **config_consola)
        self.txt_log_semantico.pack(fill=tk.BOTH, expand=True)

    def configurar_eventos(self):
        self.txt_editor.bind("<KeyRelease>", self.actualizar_lineas)
        self.txt_editor.bind("<Configure>", self.actualizar_lineas)
        self.txt_editor.bind("<MouseWheel>", self.actualizar_lineas)
        self.txt_editor.bind("<<Modified>>", self.actualizar_lineas)

    def actualizar_lineas(self, event=None):
        self.line_canvas.delete("all")
        i = self.txt_editor.index("@0,0")
        while True:
            dline = self.txt_editor.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            num_linea = str(i).split(".")[0]
            self.line_canvas.create_text(34, y, anchor="ne", text=num_linea, fill="#757575", font=("Consolas", 10))
            i = self.txt_editor.index(f"{i}+1line")
        self.txt_editor.edit_modified(False)

    def obtener_codigo(self):
        return self.txt_editor.get("1.0", tk.END).strip()

    def guardar_codigo_temporal(self):
        os.makedirs("algoritmos de prueba", exist_ok=True)
        codigo = self.obtener_codigo()
        with open(self.archivo_temporal, "w", encoding="utf-8") as f:
            f.write(codigo)

    def cargar_plantilla_inicial(self):
        plantilla = (
            "// Ejemplo inicial en Scala\n"
            "val tasaImpuesto: Float = 0.15f\n"
            "var subtotal = 100\n"
            "var total: Float = subtotal + (subtotal * tasaImpuesto)\n\n"
            "def calcularEnvio(peso: Int): Float = {\n"
            "    val tarifa: Float = 5.5f\n"
            "    return peso * tarifa\n"
            "}\n\n"
            "if (total > 100) {\n"
            "    println(\"Total a pagar: \" + total)\n"
            "}"
        )
        self.txt_editor.insert("1.0", plantilla)
        self.actualizar_lineas()

    def abrir_archivo(self):
        carpeta_inicial = "algoritmos de prueba" if os.path.isdir("algoritmos de prueba") else "."
        ruta = filedialog.askopenfilename(
            initialdir=carpeta_inicial,
            filetypes=[("Archivos Scala", "*.scala"), ("Archivos de texto", "*.txt")]
        )
        if ruta:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            self.txt_editor.delete("1.0", tk.END)
            self.txt_editor.insert("1.0", contenido)
            self.nombre_algoritmo_actual = os.path.splitext(os.path.basename(ruta))[0]
            self.actualizar_lineas()
            messagebox.showinfo("Éxito", f"Archivo cargado correctamente:\n{os.path.basename(ruta)}")

    # -----------------------------------------------------------------
    # MOTORES DE ANÁLISIS Y FORMATEO DE PANELES
    # -----------------------------------------------------------------
    def _correr_lexico(self, codigo):
        lexic_analyzer.lista_errores.clear()
        lexic_analyzer.lexer.lineno = 1
        lexic_analyzer.lexer.input(codigo)

        resultado = "TOKENS RECONOCIDOS:\n"
        resultado += "-" * 65 + "\n"
        while True:
            tok = lexic_analyzer.lexer.token()
            if not tok:
                break
            resultado += f"Línea {tok.lineno:03d} | Token: {tok.type:<22} | Valor: '{tok.value}'\n"

        resultado += "\nERRORES LÉXICOS:\n"
        resultado += "-" * 65 + "\n"
        if lexic_analyzer.lista_errores:
            for err in lexic_analyzer.lista_errores:
                resultado += f"[ERROR] {err}\n"
        else:
            resultado += "Ninguno. Análisis léxico completado sin errores.\n"

        return resultado

    def _formatear_panel_sintactico(self, errores_sintacticos):
        if errores_sintacticos:
            resultado = f"ESTADO: FALLO ({len(errores_sintacticos)} errores sintácticos encontrados)\n\n"
            for err in errores_sintacticos:
                resultado += f"[ERROR] {err}\n"
        else:
            resultado = "ESTADO: ÉXITO (0 errores sintácticos detectados).\n"
        return resultado

    def _formatear_panel_semantico(self, errores_semanticos, errores_sintacticos):
        resultado = ""
        if errores_sintacticos:
            resultado += (
                "ADVERTENCIA: Se detectaron errores sintácticos. Los resultados\n"
                "semánticos pueden estar incompletos debido a errores de estructura.\n\n"
            )
        if errores_semanticos:
            resultado += f"ESTADO: FALLO ({len(errores_semanticos)} errores semánticos encontrados)\n\n"
            for err in errores_semanticos:
                resultado += f"[ERROR] {err}\n"
        else:
            resultado += "ESTADO: ÉXITO (0 errores semánticos detectados).\n"
        return resultado

    def _correr_sintactico_y_semantico(self, codigo):
        if hasattr(syntactic_analyzer, "errores_sintacticos"):
            syntactic_analyzer.errores_sintacticos.clear()
        syntactic_analyzer.errores_semanticos.clear()
        syntactic_analyzer.tabla_simbolos["variables"].clear()
        if hasattr(syntactic_analyzer, "variables_ocultas"):
            syntactic_analyzer.variables_ocultas.clear()

        lexic_analyzer.lexer.lineno = 1
        syntactic_analyzer.parser.parse(codigo, lexer=lexic_analyzer.lexer)

        errores_sin = getattr(syntactic_analyzer, "errores_sintacticos", [])
        resultado_sin = self._formatear_panel_sintactico(errores_sin)
        resultado_sem = self._formatear_panel_semantico(
            syntactic_analyzer.errores_semanticos,
            errores_sin
        )
        return resultado_sin, resultado_sem

    # -----------------------------------------------------------------
    # BOTONES INDEPENDIENTES DE LA BARRA SUPERIOR
    # -----------------------------------------------------------------
    def ejecutar_lexico(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        resultado = self._correr_lexico(codigo)

        self.txt_log_lexico.delete("1.0", tk.END)
        self.txt_log_lexico.insert("1.0", resultado)
        self.notebook.select(self.tab_lexico)

    def ejecutar_sintactico(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        resultado_sin, resultado_sem = self._correr_sintactico_y_semantico(codigo)

        self.txt_log_sintactico.delete("1.0", tk.END)
        self.txt_log_sintactico.insert("1.0", resultado_sin)
        self.txt_log_semantico.delete("1.0", tk.END)
        self.txt_log_semantico.insert("1.0", resultado_sem)
        self.notebook.select(self.tab_sintactico)

    def ejecutar_semantico(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        resultado_sin, resultado_sem = self._correr_sintactico_y_semantico(codigo)

        self.txt_log_sintactico.delete("1.0", tk.END)
        self.txt_log_sintactico.insert("1.0", resultado_sin)
        self.txt_log_semantico.delete("1.0", tk.END)
        self.txt_log_semantico.insert("1.0", resultado_sem)
        self.notebook.select(self.tab_semantico)

    # -----------------------------------------------------------------
    # PIPELINE COMPLETO: GENERA LOS 3 LOGS REGLAMENTARIOS EN /logs/
    # -----------------------------------------------------------------
    def compilar_todo(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        resultado_lexico = self._correr_lexico(codigo)
        resultado_sin, resultado_sem = self._correr_sintactico_y_semantico(codigo)

        self.txt_log_lexico.delete("1.0", tk.END)
        self.txt_log_lexico.insert("1.0", resultado_lexico)

        self.txt_log_sintactico.delete("1.0", tk.END)
        self.txt_log_sintactico.insert("1.0", resultado_sin)

        self.txt_log_semantico.delete("1.0", tk.END)
        self.txt_log_semantico.insert("1.0", resultado_sem)

        os.makedirs("logs", exist_ok=True)
        responsable = self.responsable_var.get()
        algoritmo = self.nombre_algoritmo_actual

        archivos_generados = {
            f"lexico-{algoritmo}-{responsable}.txt": resultado_lexico,
            f"sintactico-{algoritmo}-{responsable}.txt": resultado_sin,
            f"semantico-{algoritmo}-{responsable}.txt": resultado_sem,
        }

        for nombre_archivo, contenido in archivos_generados.items():
            with open(os.path.join("logs", nombre_archivo), "w", encoding="utf-8") as f:
                f.write(contenido)

        messagebox.showinfo(
            "Compilación Completada",
            f"Análisis finalizado para las 3 fases ({responsable}).\n\n"
            f"Los logs han sido guardados en la carpeta /logs/."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCompiladorScala(root)
    root.mainloop()