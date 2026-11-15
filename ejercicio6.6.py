import tkinter as tk
from tkinter import ttk
import math

# --- BACKEND ---
class CalculosNumericos:
    @staticmethod
    def neperiano(valor: float) -> float:
        if valor <= 0:
            raise ArithmeticError("El valor debe ser estrictamente mayor a cero.")
        return math.log(valor)

    @staticmethod
    def raiz_cuadrada(valor: float) -> float:
        if valor < 0:
            raise ArithmeticError("No existe raíz cuadrada real para números negativos.")
        return math.sqrt(valor)

    @staticmethod
    def pendiente_recta(x1: float, y1: float, x2: float, y2: float) -> float:
        if x2 - x1 == 0:
            raise ZeroDivisionError("Pendiente indefinida: x1 y x2 no pueden ser iguales.")
        return (y2 - y1) / (x2 - x1)

    @staticmethod
    def punto_medio(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    @staticmethod
    def raices_cuadratica(a: float, b: float, c: float) -> tuple[float, float]:
        if a == 0:
            raise ArithmeticError("El coeficiente 'a' no puede ser cero.")
        discriminante = (b**2) - (4 * a * c)
        if discriminante < 0:
            raise ArithmeticError(f"Sin soluciones reales (discriminante = {discriminante:.2f}).")
        raiz_disc = math.sqrt(discriminante)
        return ((-b + raiz_disc) / (2 * a), (-b - raiz_disc) / (2 * a))

    @staticmethod
    def convertir_base(numero: int, base: int) -> str:
        if not (2 <= base <= 36):
            raise ValueError("La base debe estar entre 2 y 36.")
        if numero < 0:
            raise ValueError("El número debe ser un entero positivo o cero.")
        if numero == 0:
            return "0"
        
        digitos = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        resultado = []  
        while numero > 0:
            numero, residuo = divmod(numero, base)
            resultado.append(digitos[residuo])
        return "".join(reversed(resultado))


# --- FRONTEND (GUI) ---
class AppGUI:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Calculadora Numérica")
        self.raiz.geometry("500x540")
        self.raiz.resizable(False, False)

        
        self.notebook = ttk.Notebook(self.raiz)
        self.notebook.pack(expand=True, fill="both", padx=12, pady=(12, 6))

        self.tab_basicos = ttk.Frame(self.notebook, padding=15)
        self.tab_avanzados = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_basicos, text="Logaritmo y Raíz")
        self.notebook.add(self.tab_avanzados, text="Geometría, Cuadrática y Bases")

        self._construir_tab_basicos()
        self._construir_tab_avanzados()
        self._construir_panel_salida()

  
    def _construir_panel_salida(self):
        frame_out = ttk.LabelFrame(self.raiz, text="Consola de Resultado", padding=10)
        frame_out.pack(fill="x", padx=12, pady=(0, 12))

        self.lbl_titulo_res = ttk.Label(frame_out, text="Listo para calcular", font=("Segoe UI", 9, "bold"), foreground="#555555")
        self.lbl_titulo_res.pack(anchor="w")

        fila_res = ttk.Frame(frame_out)
        fila_res.pack(fill="x", pady=(4, 0))

        self.var_resultado = tk.StringVar(value="—")
        self.lbl_valor_res = ttk.Label(fila_res, textvariable=self.var_resultado, font=("Consolas", 11, "bold"), foreground="#1a5fb4")
        self.lbl_valor_res.pack(side="left", expand=True, fill="x")

        self.btn_copiar = ttk.Button(fila_res, text="Copiar", width=8, command=self._copiar_resultado, state="disabled")
        self.btn_copiar.pack(side="right")

    def _mostrar_exito(self, titulo: str, mensaje: str, valor_copiable: str):
        self.lbl_titulo_res.config(text=f"✔ {titulo}", foreground="#1e7e34")
        self.lbl_valor_res.config(foreground="#1e7e34")
        self.var_resultado.set(mensaje)
        self._ultimo_valor = valor_copiable
        self.btn_copiar.config(state="normal")

    def _mostrar_error(self, titulo: str, mensaje: str):
        self.lbl_titulo_res.config(text=f"✖ {titulo}", foreground="#c82333")
        self.lbl_valor_res.config(foreground="#c82333")
        self.var_resultado.set(mensaje)
        self.btn_copiar.config(state="disabled")

    def _copiar_resultado(self):
        self.raiz.clipboard_clear()
        self.raiz.clipboard_append(self._ultimo_valor)
        self.lbl_titulo_res.config(text="✔ Copiado al portapapeles")

    
    def _leer_floats(self, *entries: ttk.Entry) -> list[float]:
        valores = []
        for ent in entries:
            texto = ent.get().strip().replace(",", ".")  
            if not texto:
                raise ValueError("Complete todos los campos requeridos antes de calcular.")
            try:
                valores.append(float(texto))
            except ValueError:
                raise ValueError(f"'{texto}' no es un número válido.")
        return valores

    @staticmethod
    def _limpiar_entries(*entries: ttk.Entry):
        for ent in entries:
            ent.delete(0, tk.END)
        if entries:
            entries[0].focus_set()

   
    def _construir_tab_basicos(self):
        ttk.Label(self.tab_basicos, text="Ingrese un número real:", font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 4))
        
        fila_input = ttk.Frame(self.tab_basicos)
        fila_input.pack(fill="x", pady=5)

        self.ent_valor = ttk.Entry(fila_input, font=("Segoe UI", 11))
        self.ent_valor.pack(side="left", expand=True, fill="x", padx=(0, 8))
        self.ent_valor.bind("<Return>", lambda _: self.ejecutar_unario("log"))

        ttk.Button(fila_input, text="Limpiar", width=9, command=lambda: self._limpiar_entries(self.ent_valor)).pack(side="right")

        fila_btns = ttk.Frame(self.tab_basicos)
        fila_btns.pack(fill="x", pady=15)

        ttk.Button(fila_btns, text="Logaritmo Natural (Ln)", command=lambda: self.ejecutar_unario("log")).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(fila_btns, text="Raíz Cuadrada (√x)", command=lambda: self.ejecutar_unario("raiz")).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def ejecutar_unario(self, operacion: str):
        try:
            (valor,) = self._leer_floats(self.ent_valor)
            if operacion == "log":
                res = CalculosNumericos.neperiano(valor)
                self._mostrar_exito(f"ln({valor})", f"{res:.6f}", f"{res:.6f}")
            else:
                res = CalculosNumericos.raiz_cuadrada(valor)
                self._mostrar_exito(f"√({valor})", f"{res:.6f}", f"{res:.6f}")
        except (ValueError, ArithmeticError) as e:
            self._mostrar_error("Error en cálculo", str(e))

   
    def _construir_tab_avanzados(self):
        # --- 1. Geometría ---
        frame_geo = ttk.LabelFrame(self.tab_avanzados, text="Geometría Analítica: P1(x1, y1) y P2(x2, y2)", padding=8)
        frame_geo.pack(fill="x", pady=(0, 8))

        grid_geo = ttk.Frame(frame_geo)
        grid_geo.pack(fill="x")

        campos_geo = [("X1:", "ent_x1"), ("Y1:", "ent_y1"), ("X2:", "ent_x2"), ("Y2:", "ent_y2")]
        for idx, (etiqueta, attr) in enumerate(campos_geo):
            ttk.Label(grid_geo, text=etiqueta).grid(row=0, column=idx*2, padx=(4, 2))
            entry = ttk.Entry(grid_geo, width=8)
            entry.grid(row=0, column=idx*2 + 1, padx=(0, 8))
            setattr(self, attr, entry)

        entries_geo = (self.ent_x1, self.ent_y1, self.ent_x2, self.ent_y2)
        self.ent_y2.bind("<Return>", lambda _: self.ejecutar_geometria("pendiente"))

        btns_geo = ttk.Frame(frame_geo)
        btns_geo.pack(fill="x", pady=(8, 0))
        ttk.Button(btns_geo, text="Pendiente (m)", command=lambda: self.ejecutar_geometria("pendiente")).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ttk.Button(btns_geo, text="Punto Medio", command=lambda: self.ejecutar_geometria("medio")).pack(side="left", expand=True, fill="x", padx=4)
        ttk.Button(btns_geo, text="Limpiar", width=8, command=lambda: self._limpiar_entries(*entries_geo)).pack(side="right", padx=(4, 0))

       
        frame_cuad = ttk.LabelFrame(self.tab_avanzados, text="Ecuación Cuadrática (ax² + bx + c = 0)", padding=8)
        frame_cuad.pack(fill="x", pady=8)

        grid_cuad = ttk.Frame(frame_cuad)
        grid_cuad.pack(fill="x")

        for idx, (etiqueta, attr) in enumerate([("a:", "ent_a"), ("b:", "ent_b"), ("c:", "ent_c")]):
            ttk.Label(grid_cuad, text=etiqueta).pack(side="left", padx=(4, 2))
            entry = ttk.Entry(grid_cuad, width=8)
            entry.pack(side="left", padx=(0, 10))
            setattr(self, attr, entry)

        entries_cuad = (self.ent_a, self.ent_b, self.ent_c)
        self.ent_c.bind("<Return>", lambda _: self.ejecutar_cuadratica())

        ttk.Button(grid_cuad, text="Limpiar", width=8, command=lambda: self._limpiar_entries(*entries_cuad)).pack(side="right")
        ttk.Button(grid_cuad, text="Calcular Raíces", command=self.ejecutar_cuadratica).pack(side="right", padx=6)

       
        frame_base = ttk.LabelFrame(self.tab_avanzados, text="Conversión de Base (Decimal → Base b)", padding=8)
        frame_base.pack(fill="x", pady=(8, 0))

        grid_base = ttk.Frame(frame_base)
        grid_base.pack(fill="x")

        ttk.Label(grid_base, text="Entero (Base 10):").pack(side="left", padx=(4, 4))
        self.ent_numero = ttk.Entry(grid_base, width=12)
        self.ent_numero.pack(side="left", padx=(0, 12))
        self.ent_numero.bind("<Return>", lambda _: self.ejecutar_conversion())

        ttk.Label(grid_base, text="Base destino:").pack(side="left", padx=(0, 4))
        self.spin_base = ttk.Spinbox(grid_base, from_=2, to=36, width=5)
        self.spin_base.set(2)
        self.spin_base.pack(side="left", padx=(0, 10))
        self.spin_base.bind("<Return>", lambda _: self.ejecutar_conversion())

        ttk.Button(grid_base, text="Limpiar", width=8, command=lambda: self._limpiar_entries(self.ent_numero)).pack(side="right")
        ttk.Button(grid_base, text="Convertir", command=self.ejecutar_conversion).pack(side="right", padx=6)
        
    def ejecutar_geometria(self, modo: str):
        try:
            x1, y1, x2, y2 = self._leer_floats(self.ent_x1, self.ent_y1, self.ent_x2, self.ent_y2)
            if modo == "pendiente":
                res = CalculosNumericos.pendiente_recta(x1, y1, x2, y2)
                self._mostrar_exito("Pendiente (m)", f"m = {res:.4f}", f"{res:.4f}")
            else:
                xm, ym = CalculosNumericos.punto_medio(x1, y1, x2, y2)
                texto = f"({xm:.2f}, {ym:.2f})"
                self._mostrar_exito("Punto Medio", texto, texto)
        except (ValueError, ZeroDivisionError) as e:
            self._mostrar_error("Error en Geometría", str(e))

    def ejecutar_cuadratica(self):
        try:
            a, b, c = self._leer_floats(self.ent_a, self.ent_b, self.ent_c)
            x1, x2 = CalculosNumericos.raices_cuadratica(a, b, c)
            texto = f"X1 = {x1:.4f}  |  X2 = {x2:.4f}"
            self._mostrar_exito("Raíces Reales", texto, f"{x1:.4f}, {x2:.4f}")
        except (ValueError, ArithmeticError) as e:
            self._mostrar_error("Error en Cuadrática", str(e))

    def ejecutar_conversion(self):
        try:
            num_txt = self.ent_numero.get().strip()
            base_txt = self.spin_base.get().strip()
            if not num_txt or not base_txt:
                raise ValueError("Ingrese el número entero y la base destino.")
            
            try:
                numero = int(num_txt)
                base = int(base_txt)
            except ValueError:
                raise ValueError("Tanto el número como la base deben ser enteros sin decimales.")

            res = CalculosNumericos.convertir_base(numero, base)
            self._mostrar_exito(f"{numero}₁₀ en Base {base}", res, res)
        except ValueError as e:
            self._mostrar_error("Error de Conversión", str(e))


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AppGUI(raiz)
    raiz.mainloop()