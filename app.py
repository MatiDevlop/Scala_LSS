import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Importación del motor del compilador desarrollado por el grupo
import lexic_analyzer
import syntactic_analyzer


# ---------------------------------------------------------------------
# SISTEMA DE DISEÑO (tema oscuro único y consistente)
# Todos los colores de texto cumplen contraste >= 4.5:1 (WCAG AA)
# sobre su fondo. Los colores semánticos se reservan para estados:
# verde = éxito, rojo = error, ámbar = advertencia, azul = acción/encabezado.
# ---------------------------------------------------------------------
COLORES = {
    "bg_app": "#14161b",       # fondo de la ventana
    "bg_panel": "#1c1f26",     # paneles y barra de herramientas
    "bg_editor": "#1a1d23",    # área de escritura / logs
    "bg_gutter": "#15171c",    # margen de números de línea
    "borde": "#2e333d",        # bordes sutiles
    "texto": "#e6e8ee",        # texto principal
    "texto_suave": "#9aa3b2",  # texto secundario / etiquetas
    "linea_num": "#7d8696",    # números de línea
    "btn": "#2a2f3a",          # botón secundario
    "btn_hover": "#373e4d",
    "btn_press": "#444c5e",
    "accent": "#2563eb",       # acción principal
    "accent_hover": "#3b78f5",
    "accent_press": "#1d4ed8",
    "seleccion": "#33507f",    # selección de texto
    "exito": "#4ade80",
    "error": "#f87171",
    "aviso": "#fbbf24",
    "info": "#7db4ff",
}

FUENTE_UI = ("Segoe UI", 10)
FUENTE_UI_NEGRITA = ("Segoe UI", 10, "bold")
FUENTE_TITULO = ("Segoe UI Semibold", 10)
FUENTE_CODIGO = ("Consolas", 12)
FUENTE_LOG = ("Consolas", 11)


class InterfazCompiladorScala:
    def __init__(self, root):
        self.root = root
        self.root.title("Scala LSS Compiler IDE - Panel de Control")
        self.root.geometry("1280x760")
        self.root.minsize(1050, 620)
        self.root.configure(bg=COLORES["bg_app"])

        self.responsable_var = tk.StringVar(value="KevinMorocho")
        self.nombre_algoritmo_actual = "workspace_gui"
        self.archivo_temporal = os.path.join("algoritmos de prueba", "workspace_gui.scala")

        self.aplicar_estilos()
        self.crear_componentes()
        self.configurar_eventos()
        self.cargar_plantilla_inicial()

    # -----------------------------------------------------------------
    # ESTILOS GLOBALES (solo apariencia)
    # -----------------------------------------------------------------
    def aplicar_estilos(self):
        c = COLORES
        style = ttk.Style()
        style.theme_use("clam")

        # Lista desplegable del Combobox (no es un widget ttk)
        self.root.option_add("*TCombobox*Listbox.background", c["bg_panel"])
        self.root.option_add("*TCombobox*Listbox.foreground", c["texto"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", c["accent"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
        self.root.option_add("*TCombobox*Listbox.font", FUENTE_UI)

        style.configure(".", background=c["bg_app"], foreground=c["texto"], font=FUENTE_UI)

        # Contenedores
        style.configure("TFrame", background=c["bg_app"])
        style.configure("Toolbar.TFrame", background=c["bg_panel"])
        style.configure("Card.TFrame", background=c["bg_panel"])
        style.configure("TPanedwindow", background=c["bg_app"])

        style.configure(
            "Card.TLabelframe",
            background=c["bg_panel"],
            bordercolor=c["borde"],
            lightcolor=c["borde"],
            darkcolor=c["borde"],
            relief="solid",
            borderwidth=1,
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=c["bg_panel"],
            foreground=c["info"],
            font=FUENTE_TITULO,
        )

        # Etiquetas y separadores
        style.configure("Toolbar.TLabel", background=c["bg_panel"], foreground=c["texto_suave"], font=FUENTE_UI)
        style.configure("TSeparator", background=c["borde"])

        # Botones secundarios (grandes, para facilitar el clic: ley de Fitts)
        style.configure(
            "TButton",
            background=c["btn"],
            foreground=c["texto"],
            bordercolor=c["borde"],
            lightcolor=c["btn"],
            darkcolor=c["btn"],
            focuscolor=c["info"],
            font=FUENTE_UI,
            padding=(14, 8),
            relief="flat",
            borderwidth=1,
        )
        style.map(
            "TButton",
            background=[("pressed", c["btn_press"]), ("active", c["btn_hover"])],
            lightcolor=[("pressed", c["btn_press"]), ("active", c["btn_hover"])],
            darkcolor=[("pressed", c["btn_press"]), ("active", c["btn_hover"])],
            bordercolor=[("focus", c["info"])],
        )

        # Botón de acción principal (jerarquía visual: único elemento de color fuerte)
        style.configure(
            "Accent.TButton",
            background=c["accent"],
            foreground="#ffffff",
            bordercolor=c["accent"],
            lightcolor=c["accent"],
            darkcolor=c["accent"],
            font=("Segoe UI", 10, "bold"),
            padding=(18, 8),
        )
        style.map(
            "Accent.TButton",
            background=[("pressed", c["accent_press"]), ("active", c["accent_hover"])],
            lightcolor=[("pressed", c["accent_press"]), ("active", c["accent_hover"])],
            darkcolor=[("pressed", c["accent_press"]), ("active", c["accent_hover"])],
            bordercolor=[("focus", "#ffffff")],
        )

        # Combobox
        style.configure(
            "TCombobox",
            fieldbackground=c["btn"],
            background=c["btn"],
            foreground=c["texto"],
            arrowcolor=c["texto"],
            bordercolor=c["borde"],
            lightcolor=c["btn"],
            darkcolor=c["btn"],
            selectbackground=c["btn"],
            selectforeground=c["texto"],
            padding=6,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", c["btn"])],
            foreground=[("readonly", c["texto"])],
            selectbackground=[("readonly", c["btn"])],
            selectforeground=[("readonly", c["texto"])],
            bordercolor=[("focus", c["info"])],
        )

        # Pestañas
        style.configure("TNotebook", background=c["bg_panel"], borderwidth=0, tabmargins=(0, 4, 0, 0))
        style.configure(
            "TNotebook.Tab",
            background=c["bg_app"],
            foreground=c["texto_suave"],
            padding=(18, 9),
            font=FUENTE_UI,
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", c["accent"]), ("active", c["btn_hover"])],
            foreground=[("selected", "#ffffff"), ("active", c["texto"])],
            font=[("selected", FUENTE_UI_NEGRITA)],
        )

        # Barras de desplazamiento discretas
        for orient in ("Vertical", "Horizontal"):
            style.configure(
                f"{orient}.TScrollbar",
                background=c["btn_hover"],
                troughcolor=c["bg_gutter"],
                bordercolor=c["bg_gutter"],
                lightcolor=c["btn_hover"],
                darkcolor=c["btn_hover"],
                arrowcolor=c["texto_suave"],
                relief="flat",
                gripcount=0,
            )
            style.map(
                f"{orient}.TScrollbar",
                background=[("pressed", c["btn_press"]), ("active", c["btn_press"])],
            )

    def crear_componentes(self):
        c = COLORES

        # -----------------------------------------------------------------
        # 1. BARRA DE HERRAMIENTAS SUPERIOR (BOTONES DE ACCIÓN)
        #    Agrupada por proximidad: archivo | fases | compilación total
        # -----------------------------------------------------------------
        toolbar = ttk.Frame(self.root, padding=(12, 10), style="Toolbar.TFrame")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open = ttk.Button(toolbar, text="Abrir Archivo (.scala)", command=self.abrir_archivo)
        btn_open.pack(side=tk.LEFT, padx=(0, 6))

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=12)

        btn_lex = ttk.Button(toolbar, text="Analizar Léxico", command=self.ejecutar_lexico)
        btn_lex.pack(side=tk.LEFT, padx=3)

        btn_sin = ttk.Button(toolbar, text="Analizar Sintáctico", command=self.ejecutar_sintactico)
        btn_sin.pack(side=tk.LEFT, padx=3)

        btn_sem = ttk.Button(toolbar, text="Analizar Semántico", command=self.ejecutar_semantico)
        btn_sem.pack(side=tk.LEFT, padx=3)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=12)

        btn_all = ttk.Button(toolbar, text="▶  COMPILAR TODO", style="Accent.TButton", command=self.compilar_todo)
        btn_all.pack(side=tk.LEFT, padx=3)

        # Selector de responsable del log a la derecha
        combo_resp = ttk.Combobox(
            toolbar,
            textvariable=self.responsable_var,
            values=["KevinMorocho", "DavidOlvera"],
            state="readonly",
            width=18,
            font=FUENTE_UI,
        )
        combo_resp.pack(side=tk.RIGHT, padx=(6, 0))
        ttk.Label(toolbar, text="Responsable Log:", style="Toolbar.TLabel").pack(side=tk.RIGHT, padx=6)

        # -----------------------------------------------------------------
        # 2. PANEL PRINCIPAL DIVIDIDO (LADO A LADO)
        # -----------------------------------------------------------------
        panel_dividido = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        panel_dividido.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- LADO IZQUIERDO: EDITOR DE CÓDIGO SCALA ---
        frame_izquierdo = ttk.LabelFrame(
            panel_dividido, text=" Editor de Código Scala ", padding=8, style="Card.TLabelframe"
        )
        panel_dividido.add(frame_izquierdo, weight=1)

        contenedor_editor = ttk.Frame(frame_izquierdo, style="Card.TFrame")
        contenedor_editor.pack(fill=tk.BOTH, expand=True)

        self.line_canvas = tk.Canvas(
            contenedor_editor, width=46, bg=c["bg_gutter"], bd=0, highlightthickness=0
        )
        self.line_canvas.pack(side=tk.LEFT, fill=tk.Y)

        scroll_y = ttk.Scrollbar(contenedor_editor)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_editor = tk.Text(
            contenedor_editor,
            wrap=tk.NONE,
            yscrollcommand=scroll_y.set,
            font=FUENTE_CODIGO,
            undo=True,
            bg=c["bg_editor"],
            fg=c["texto"],
            insertbackground=c["texto"],
            insertwidth=2,
            selectbackground=c["seleccion"],
            selectforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=6,
        )
        self.txt_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.txt_editor.yview)

        scroll_x = ttk.Scrollbar(frame_izquierdo, orient=tk.HORIZONTAL, command=self.txt_editor.xview)
        self.txt_editor.config(xscrollcommand=scroll_x.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # --- LADO DERECHO: CENTRO DE DIAGNÓSTICO (LOGS) ---
        frame_derecho = ttk.LabelFrame(
            panel_dividido, text=" Diagnóstico y Reportes del Sistema ", padding=8, style="Card.TLabelframe"
        )
        panel_dividido.add(frame_derecho, weight=1)

        self.notebook = ttk.Notebook(frame_derecho)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        config_consola = {
            "bg": c["bg_editor"],
            "fg": c["texto"],
            "insertbackground": c["texto"],
            "selectbackground": c["seleccion"],
            "selectforeground": "#ffffff",
            "font": FUENTE_LOG,
            "wrap": tk.WORD,
            "relief": tk.FLAT,
            "bd": 0,
            "highlightthickness": 0,
            "padx": 12,
            "pady": 10,
            "spacing1": 2,
            "spacing3": 2,
        }

        # Pestaña 1: Log Léxico
        self.tab_lexico = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.tab_lexico, text=" Log Léxico ")
        self.txt_log_lexico = tk.Text(self.tab_lexico, **config_consola)
        self.txt_log_lexico.pack(fill=tk.BOTH, expand=True)

        # Pestaña 2: Log Sintáctico
        self.tab_sintactico = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.tab_sintactico, text=" Log Sintáctico ")
        self.txt_log_sintactico = tk.Text(self.tab_sintactico, **config_consola)
        self.txt_log_sintactico.pack(fill=tk.BOTH, expand=True)

        # Pestaña 3: Log Semántico
        self.tab_semantico = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.tab_semantico, text=" Log Semántico ")
        self.txt_log_semantico = tk.Text(self.tab_semantico, **config_consola)
        self.txt_log_semantico.pack(fill=tk.BOTH, expand=True)

        # Etiquetas de color para los logs (feedback visual por estado)
        for txt in (self.txt_log_lexico, self.txt_log_sintactico, self.txt_log_semantico):
            txt.tag_configure("titulo", foreground=c["info"], font=("Consolas", 11, "bold"))
            txt.tag_configure("separador", foreground=c["borde"])
            txt.tag_configure("exito", foreground=c["exito"], font=("Consolas", 11, "bold"))
            txt.tag_configure("error", foreground=c["error"])
            txt.tag_configure("fallo", foreground=c["error"], font=("Consolas", 11, "bold"))
            txt.tag_configure("aviso", foreground=c["aviso"])

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
            self.line_canvas.create_text(
                40, y, anchor="ne", text=num_linea, fill=COLORES["linea_num"], font=FUENTE_CODIGO
            )
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
    # PRESENTACIÓN DE LOGS (solo colorea el texto; el contenido no cambia)
    # -----------------------------------------------------------------
    def _mostrar_log(self, widget, texto):
        widget.delete("1.0", tk.END)
        widget.insert("1.0", texto)

        for n, linea in enumerate(texto.split("\n"), start=1):
            etiqueta = None
            if linea.startswith("[ERROR]"):
                etiqueta = "error"
            elif linea.startswith("ESTADO: ÉXITO") or linea.startswith("Ninguno."):
                etiqueta = "exito"
            elif linea.startswith("ESTADO: FALLO"):
                etiqueta = "fallo"
            elif linea.startswith("ADVERTENCIA") or linea.startswith("semánticos pueden"):
                etiqueta = "aviso"
            elif linea.endswith(":") and linea.isupper():
                etiqueta = "titulo"
            elif linea and set(linea) == {"-"}:
                etiqueta = "separador"
            if etiqueta:
                widget.tag_add(etiqueta, f"{n}.0", f"{n}.end")

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

        self._mostrar_log(self.txt_log_lexico, resultado)
        self.notebook.select(self.tab_lexico)

    def ejecutar_sintactico(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        resultado_sin, resultado_sem = self._correr_sintactico_y_semantico(codigo)

        self._mostrar_log(self.txt_log_sintactico, resultado_sin)
        self._mostrar_log(self.txt_log_semantico, resultado_sem)
        self.notebook.select(self.tab_sintactico)

    def ejecutar_semantico(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        resultado_sin, resultado_sem = self._correr_sintactico_y_semantico(codigo)

        self._mostrar_log(self.txt_log_sintactico, resultado_sin)
        self._mostrar_log(self.txt_log_semantico, resultado_sem)
        self.notebook.select(self.tab_semantico)

    # -----------------------------------------------------------------
    # PIPELINE COMPLETO: GENERA LOS 3 LOGS REGLAMENTARIOS EN /logs/
    # -----------------------------------------------------------------
    def compilar_todo(self):
        codigo = self.obtener_codigo()
        self.guardar_codigo_temporal()

        resultado_lexico = self._correr_lexico(codigo)
        resultado_sin, resultado_sem = self._correr_sintactico_y_semantico(codigo)

        self._mostrar_log(self.txt_log_lexico, resultado_lexico)
        self._mostrar_log(self.txt_log_sintactico, resultado_sin)
        self._mostrar_log(self.txt_log_semantico, resultado_sem)

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