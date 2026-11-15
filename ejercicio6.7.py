import tkinter as tk
from tkinter import ttk


# backend

class EquipoCompletoError(Exception):
    pass


class FormatoTextoInvalidoError(Exception):
    pass


class ContrasenaError(Exception):
    pass


class ContrasenasNoCoincidenError(ContrasenaError):
    pass


class RequisitosContrasenaError(ContrasenaError):
    pass


class Programador:
    def __init__(self, nombre: str, apellidos: str):
        self.validar_atributos(nombre, apellidos)
        self.nombre = nombre.strip()
        self.apellidos = apellidos.strip()

    @staticmethod
    def validar_atributos(nombre: str, apellidos: str) -> None:
        for campo, valor in (("Nombre", nombre), ("Apellidos", apellidos)):
            if not isinstance(valor, str):
                raise TypeError(f"El campo '{campo}' debe ser una cadena de texto.")

            valor_limpio = valor.strip()
            if not valor_limpio:
                raise ValueError(f"El campo '{campo}' no puede estar vacío.")

            if len(valor_limpio) >= 20:
                raise ValueError(
                    f"El campo '{campo}' debe tener menos de 20 caracteres (actual: {len(valor_limpio)})."
                )

            if any(char.isdigit() for char in valor_limpio):
                raise FormatoTextoInvalidoError(f"El campo '{campo}' no puede contener números.")

            if not all(char.isalpha() or char.isspace() for char in valor_limpio):
                raise FormatoTextoInvalidoError(f"El campo '{campo}' solo debe contener letras.")

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellidos}"


class EquipoMaratonProgramacion:
    def __init__(self, nombre: str, universidad: str, lenguaje_programacion: str, tamano: int):
        if not isinstance(tamano, int):
            raise TypeError("El tamaño del equipo debe ser un número entero.")
        if not (2 <= tamano <= 3):
            raise ValueError("El tamaño del equipo debe ser mínimo 2 y máximo 3 programadores.")
        if not all(isinstance(c, str) and c.strip() for c in (nombre, universidad, lenguaje_programacion)):
            raise ValueError("Nombre del equipo, universidad y lenguaje son obligatorios.")

        self.nombre = nombre.strip()
        self.universidad = universidad.strip()
        self.lenguaje_programacion = lenguaje_programacion.strip()
        self.tamano = tamano
        self.miembros: list[Programador] = []

    def esta_completo(self) -> bool:
        return len(self.miembros) >= self.tamano

    def anadir_programador(self, programador: Programador) -> None:
        if self.esta_completo():
            raise EquipoCompletoError(
                f"El equipo '{self.nombre}' ya está lleno ({self.tamano}/{self.tamano} cupos)."
            )
        if not isinstance(programador, Programador):
            raise TypeError("Solo se pueden añadir instancias válidas de Programador.")

        self.miembros.append(programador)


class Contrasena:
    def __init__(self, password: str, confirmacion: str):
        self.validar(password, confirmacion)
        self._valor = password

    @staticmethod
    def validar(password: str, confirmacion: str) -> None:
        if not isinstance(password, str) or not isinstance(confirmacion, str):
            raise TypeError("Las contraseñas deben ser cadenas de texto.")

        if password != confirmacion:
            raise ContrasenasNoCoincidenError("Las contraseñas ingresadas no coinciden.")

        if len(password) < 8:
            raise RequisitosContrasenaError(
                f"La contraseña debe tener mínimo 8 caracteres (actual: {len(password)})."
            )

        # Recorro el texto una sola vez para revisar todas las reglas
        tiene_minuscula = False
        tiene_mayuscula = False
        tiene_numero = False
        tiene_especial = False

        for char in password:
            if char.isspace():
                raise RequisitosContrasenaError("La contraseña no debe contener espacios en blanco.")
            elif char.islower():
                tiene_minuscula = True
            elif char.isupper():
                tiene_mayuscula = True
            elif char.isdigit():
                tiene_numero = True
            elif not char.isalnum():
                tiene_especial = True

        faltantes = []
        if not tiene_minuscula:
            faltantes.append("una letra minúscula")
        if not tiene_mayuscula:
            faltantes.append("una letra mayúscula")
        if not tiene_numero:
            faltantes.append("un número")
        if not tiene_especial:
            faltantes.append("un carácter especial (ej. @, #, $, %)")

        if faltantes:
            raise RequisitosContrasenaError(f"Falta incluir al menos: {', '.join(faltantes)}.")

    def __str__(self) -> str:
        # Enmascaro la salida para no imprimir la clave en texto plano
        return "*" * len(self._valor)


# frontend

class AppTallerGUI:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Taller 4 - Equipos de Maratón y Validación de Claves")
        self.raiz.geometry("540x600")
        self.raiz.resizable(False, False)

        self.equipo_actual: EquipoMaratonProgramacion | None = None
        self.clave_registrada: Contrasena | None = None

        self.notebook = ttk.Notebook(self.raiz)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_maraton = ttk.Frame(self.notebook, padding=10)
        self.tab_password = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.tab_maraton, text="1. Equipo Maratón")
        self.notebook.add(self.tab_password, text="2. Validador de Contraseña")

        self._construir_tab_maraton()
        self._construir_tab_password()

        # Bloqueo el registro de integrantes hasta que exista un equipo válido
        self._cambiar_estado_contenedor(self.frame_prog, "disabled")

    # pestaña 1: equipo maratón

    def _construir_tab_maraton(self):
        self.frame_equipo = ttk.LabelFrame(self.tab_maraton, text="1. Configuración del equipo", padding=10)
        self.frame_equipo.pack(fill="x", pady=(0, 8))
        self.frame_equipo.columnconfigure(1, weight=1)

        ttk.Label(self.frame_equipo, text="Nombre del equipo:").grid(row=0, column=0, sticky="w", pady=3)
        self.ent_equipo = ttk.Entry(self.frame_equipo)
        self.ent_equipo.grid(row=0, column=1, columnspan=3, sticky="ew", padx=(8, 0), pady=3)

        ttk.Label(self.frame_equipo, text="Universidad:").grid(row=1, column=0, sticky="w", pady=3)
        self.ent_uni = ttk.Entry(self.frame_equipo)
        self.ent_uni.grid(row=1, column=1, columnspan=3, sticky="ew", padx=(8, 0), pady=3)

        ttk.Label(self.frame_equipo, text="Lenguaje:").grid(row=2, column=0, sticky="w", pady=3)
        self.combo_lenguaje = ttk.Combobox(
            self.frame_equipo,
            values=["Python", "Java", "C++", "C#", "JavaScript"],
            width=18
        )
        self.combo_lenguaje.grid(row=2, column=1, sticky="w", padx=(8, 12), pady=3)

        ttk.Label(self.frame_equipo, text="Cupos (2-3):").grid(row=2, column=2, sticky="e", pady=3)
        self.spin_tamano = ttk.Spinbox(self.frame_equipo, from_=2, to=3, width=5)
        self.spin_tamano.set(2)
        self.spin_tamano.grid(row=2, column=3, sticky="e", padx=(6, 0), pady=3)

        fila_btns = ttk.Frame(self.frame_equipo)
        fila_btns.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(8, 0))

        self.btn_crear_equipo = ttk.Button(fila_btns, text="Crear equipo", command=self.ejecutar_crear_equipo)
        self.btn_crear_equipo.pack(side="left", expand=True, fill="x", padx=(0, 4))

        self.btn_reiniciar = ttk.Button(fila_btns, text="Nuevo / Reiniciar", command=self.reiniciar_todo)
        self.btn_reiniciar.pack(side="right", padx=(4, 0))

        self.frame_prog = ttk.LabelFrame(
            self.tab_maraton, text="2. Añadir programador (máx. 19 caracteres, solo letras)", padding=10
        )
        self.frame_prog.pack(fill="x", pady=8)
        self.frame_prog.columnconfigure(1, weight=1)
        self.frame_prog.columnconfigure(3, weight=1)

        ttk.Label(self.frame_prog, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.ent_nombre_prog = ttk.Entry(self.frame_prog)
        self.ent_nombre_prog.grid(row=0, column=1, sticky="ew", padx=(5, 10))

        ttk.Label(self.frame_prog, text="Apellidos:").grid(row=0, column=2, sticky="w")
        self.ent_apellidos_prog = ttk.Entry(self.frame_prog)
        self.ent_apellidos_prog.grid(row=0, column=3, sticky="ew", padx=(5, 0))
        self.ent_apellidos_prog.bind("<Return>", lambda _: self.ejecutar_anadir_programador())

        self.btn_anadir_prog = ttk.Button(
            self.frame_prog, text="Añadir programador al equipo", command=self.ejecutar_anadir_programador
        )
        self.btn_anadir_prog.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(10, 0))

        frame_lista = ttk.LabelFrame(self.tab_maraton, text="3. Nómina del equipo", padding=10)
        frame_lista.pack(fill="both", expand=True, pady=8)

        barra_info = ttk.Frame(frame_lista)
        barra_info.pack(fill="x", pady=(0, 6))

        self.var_cupos = tk.StringVar(value="Cupos: 0 / 0")
        ttk.Label(barra_info, textvariable=self.var_cupos, font=("Segoe UI", 9, "bold")).pack(side="left")

        self.var_estado_equipo = tk.StringVar(value="SIN EQUIPO")
        self.lbl_badge_estado = ttk.Label(
            barra_info, textvariable=self.var_estado_equipo, font=("Segoe UI", 9, "bold"), foreground="#666666"
        )
        self.lbl_badge_estado.pack(side="right")

        self.lista_miembros = tk.Listbox(frame_lista, height=4, font=("Consolas", 10), activestyle="none")
        self.lista_miembros.pack(fill="both", expand=True)

        frame_out = ttk.LabelFrame(self.tab_maraton, text="Estado / errores", padding=8)
        frame_out.pack(fill="x", pady=(4, 0))

        self.var_msg_equipo = tk.StringVar(value="Configure los datos del equipo para comenzar.")
        self.lbl_msg_equipo = ttk.Label(
            frame_out, textvariable=self.var_msg_equipo,
            font=("Segoe UI", 9, "bold"), foreground="#333333", wraplength=475
        )
        self.lbl_msg_equipo.pack(anchor="w")

    # pestaña 2: validador de contraseña

    def _construir_tab_password(self):
        frame_reglas = ttk.LabelFrame(self.tab_password, text="Requisitos de la contraseña", padding=10)
        frame_reglas.pack(fill="x", pady=(0, 12))

        reglas_texto = (
            "• Mínimo 8 caracteres y sin espacios en blanco.\n"
            "• Al menos: 1 minúscula, 1 mayúscula, 1 número y 1 símbolo.\n"
            "• Ambas entradas deben coincidir exactamente."
        )
        ttk.Label(frame_reglas, text=reglas_texto, font=("Segoe UI", 9), foreground="#444444").pack(anchor="w")

        frame_form = ttk.LabelFrame(self.tab_password, text="Ingreso y confirmación", padding=12)
        frame_form.pack(fill="x", pady=8)
        frame_form.columnconfigure(1, weight=1)

        ttk.Label(frame_form, text="Contraseña:").grid(row=0, column=0, sticky="w", pady=6)
        self.ent_pwd1 = ttk.Entry(frame_form, show="*", font=("Consolas", 10))
        self.ent_pwd1.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=6)
        self.ent_pwd1.bind("<Return>", lambda _: self.ent_pwd2.focus_set())

        ttk.Label(frame_form, text="Confirmar contraseña:").grid(row=1, column=0, sticky="w", pady=6)
        self.ent_pwd2 = ttk.Entry(frame_form, show="*", font=("Consolas", 10))
        self.ent_pwd2.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=6)
        self.ent_pwd2.bind("<Return>", lambda _: self.ejecutar_validar_contrasena())

        self.var_mostrar_pwd = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame_form,
            text="Mostrar contraseñas",
            variable=self.var_mostrar_pwd,
            command=self._alternar_visibilidad_clave
        ).grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(2, 8))

        fila_btns_pwd = ttk.Frame(frame_form)
        fila_btns_pwd.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(4, 0))

        ttk.Button(
            fila_btns_pwd, text="Validar contraseña", command=self.ejecutar_validar_contrasena
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            fila_btns_pwd, text="Limpiar", width=12, command=self.limpiar_contrasena
        ).pack(side="right", padx=(5, 0))

        frame_out_pwd = ttk.LabelFrame(self.tab_password, text="Resultado de validación", padding=10)
        frame_out_pwd.pack(fill="x", pady=(12, 0))

        self.var_msg_pwd = tk.StringVar(value="Ingrese y confirme una contraseña para validar.")
        self.lbl_msg_pwd = ttk.Label(
            frame_out_pwd, textvariable=self.var_msg_pwd,
            font=("Segoe UI", 9, "bold"), foreground="#333333", wraplength=475
        )
        self.lbl_msg_pwd.pack(anchor="w")

    # helpers

    def _cambiar_estado_contenedor(self, contenedor: ttk.LabelFrame, estado: str):
        # Recorro también los frames internos para activar o bloquear todos los controles
        def _aplicar_recursivo(widget):
            if "state" in widget.keys():
                widget.configure(state=estado)
            for hijo in widget.winfo_children():
                _aplicar_recursivo(hijo)

        _aplicar_recursivo(contenedor)

    @staticmethod
    def _notificar(var_destino: tk.StringVar, lbl_destino: ttk.Label, texto: str, es_error: bool = False):
        color = "#c82333" if es_error else "#1e7e34"
        prefijo = "✖ " if es_error else "✔ "
        lbl_destino.config(foreground=color)
        var_destino.set(f"{prefijo}{texto}")

    # controladores maratón

    def _actualizar_nomina_ui(self):
        self.lista_miembros.delete(0, tk.END)
        if not self.equipo_actual:
            self.var_cupos.set("Cupos: 0 / 0")
            self.var_estado_equipo.set("SIN EQUIPO")
            self.lbl_badge_estado.config(foreground="#666666")
            return

        actual = len(self.equipo_actual.miembros)
        total = self.equipo_actual.tamano
        self.var_cupos.set(
            f"Equipo: {self.equipo_actual.nombre} ({self.equipo_actual.lenguaje_programacion})  |  Cupos: {actual} / {total}"
        )

        for idx, miembro in enumerate(self.equipo_actual.miembros, start=1):
            self.lista_miembros.insert(tk.END, f"  {idx}. {miembro}")

        if self.equipo_actual.esta_completo():
            self.var_estado_equipo.set("EQUIPO COMPLETO")
            self.lbl_badge_estado.config(foreground="#1e7e34")
        else:
            self.var_estado_equipo.set("INCOMPLETO")
            self.lbl_badge_estado.config(foreground="#d97706")

    def ejecutar_crear_equipo(self):
        if self.equipo_actual is not None:
            self._notificar(
                self.var_msg_equipo,
                self.lbl_msg_equipo,
                "Ya existe un equipo activo. Reinicie para crear otro.",
                es_error=True
            )
            return

        try:
            nombre = self.ent_equipo.get()
            uni = self.ent_uni.get()
            lenguaje = self.combo_lenguaje.get()
            tam_txt = self.spin_tamano.get().strip()

            try:
                tamano = int(tam_txt)
            except ValueError:
                raise ValueError("El tamaño del equipo debe ser un número entero.")

            self.equipo_actual = EquipoMaratonProgramacion(nombre, uni, lenguaje, tamano)

            self._cambiar_estado_contenedor(self.frame_equipo, "disabled")
            self.btn_reiniciar.configure(state="normal")
            self._cambiar_estado_contenedor(self.frame_prog, "normal")

            self._actualizar_nomina_ui()
            self._notificar(
                self.var_msg_equipo,
                self.lbl_msg_equipo,
                f"Equipo '{self.equipo_actual.nombre}' creado. Ingrese los {tamano} integrantes."
            )
            self.ent_nombre_prog.focus_set()

        except (ValueError, TypeError) as error:
            self._notificar(self.var_msg_equipo, self.lbl_msg_equipo, str(error), es_error=True)

    def ejecutar_anadir_programador(self):
        if not self.equipo_actual:
            return

        try:
            nom = self.ent_nombre_prog.get()
            ape = self.ent_apellidos_prog.get()

            if self.equipo_actual.esta_completo():
                raise EquipoCompletoError(
                    f"El equipo '{self.equipo_actual.nombre}' ya está lleno ({self.equipo_actual.tamano}/{self.equipo_actual.tamano})."
                )

            nuevo_prog = Programador(nom, ape)
            self.equipo_actual.anadir_programador(nuevo_prog)

            self._actualizar_nomina_ui()
            self.ent_nombre_prog.delete(0, tk.END)
            self.ent_apellidos_prog.delete(0, tk.END)
            self.ent_nombre_prog.focus_set()

            if self.equipo_actual.esta_completo():
                msg = f"{nuevo_prog} añadido. El equipo ya está completo."
            else:
                msg = f"{nuevo_prog} añadido al equipo."
            self._notificar(self.var_msg_equipo, self.lbl_msg_equipo, msg)

        except (ValueError, FormatoTextoInvalidoError, EquipoCompletoError) as error:
            self._notificar(self.var_msg_equipo, self.lbl_msg_equipo, str(error), es_error=True)

    def reiniciar_todo(self):
        self.equipo_actual = None
        self._cambiar_estado_contenedor(self.frame_equipo, "normal")

        for widget in (
            self.ent_equipo, self.ent_uni, self.combo_lenguaje,
            self.ent_nombre_prog, self.ent_apellidos_prog
        ):
            widget.delete(0, tk.END)
        self.spin_tamano.set(2)

        self._cambiar_estado_contenedor(self.frame_prog, "disabled")
        self._actualizar_nomina_ui()
        self.lbl_msg_equipo.config(foreground="#333333")
        self.var_msg_equipo.set("Formulario reiniciado. Configure un nuevo equipo.")
        self.ent_equipo.focus_set()

    # controladores contraseña

    def _alternar_visibilidad_clave(self):
        caracter = "" if self.var_mostrar_pwd.get() else "*"
        self.ent_pwd1.configure(show=caracter)
        self.ent_pwd2.configure(show=caracter)

    def ejecutar_validar_contrasena(self):
        try:
            pwd1 = self.ent_pwd1.get()
            pwd2 = self.ent_pwd2.get()

            self.clave_registrada = Contrasena(pwd1, pwd2)
            self._notificar(
                self.var_msg_pwd,
                self.lbl_msg_pwd,
                f"Contraseña válida y registrada ({self.clave_registrada})."
            )

        except ContrasenaError as error:
            self.clave_registrada = None
            self._notificar(self.var_msg_pwd, self.lbl_msg_pwd, str(error), es_error=True)

    def limpiar_contrasena(self):
        self.clave_registrada = None
        self.ent_pwd1.delete(0, tk.END)
        self.ent_pwd2.delete(0, tk.END)
        self.lbl_msg_pwd.config(foreground="#333333")
        self.var_msg_pwd.set("Campos limpios. Ingrese una nueva contraseña.")
        self.ent_pwd1.focus_set()


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AppTallerGUI(raiz)
    raiz.mainloop()