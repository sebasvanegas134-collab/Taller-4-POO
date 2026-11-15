import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path


# backend

class ErrorLecturaArchivo(Exception):
    pass


class LeerArchivo:
    def __init__(self, ruta_archivo: str = "prueba.txt"):
        if not isinstance(ruta_archivo, str):
            raise TypeError("La ruta del archivo debe ser una cadena de texto.")

        ruta_limpia = ruta_archivo.strip()
        if not ruta_limpia:
            raise ValueError("El nombre o ruta del archivo no puede estar vacío.")

        ruta_candidata = Path(ruta_limpia)

        # Si es relativa, busco primero junto al script para que sea reproducible
        if not ruta_candidata.is_absolute():
            ruta_script = Path(__file__).resolve().parent / ruta_candidata
            if ruta_script.exists():
                ruta_candidata = ruta_script

        self.ruta = ruta_candidata

        if not self.ruta.exists():
            raise FileNotFoundError(f"No se encontró el archivo: '{self.ruta}'.")
        if not self.ruta.is_file():
            raise IsADirectoryError(f"La ruta '{self.ruta}' es un directorio, no un archivo.")

    def leer_contenido(self) -> str:
        # Leo en bytes y decodifico por línea para poder reportar la línea exacta
        # si el archivo no es UTF-8 válido. El join final es O(N) sobre el total.
        lineas: list[str] = []

        try:
            with open(self.ruta, mode="rb") as flujo:
                for numero_linea, linea_bytes in enumerate(flujo, start=1):
                    try:
                        lineas.append(linea_bytes.decode("utf-8"))
                    except UnicodeDecodeError as e:
                        raise ErrorLecturaArchivo(
                            f"El archivo no contiene texto UTF-8 válido en la línea {numero_linea}."
                        ) from e
        except PermissionError as e:
            raise PermissionError(f"Permiso denegado para leer '{self.ruta}'.") from e

        return "".join(lineas)

    def leer_en_mayusculas(self) -> str:
        return self.leer_contenido().upper()


# frontend

class AppLectorArchivoGUI:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Lector de Archivos - Flujo de Bytes")
        self.raiz.geometry("640x520")
        self.raiz.minsize(560, 460)

        self._texto_actual: str = ""

        contenedor = ttk.Frame(self.raiz, padding=12)
        contenedor.pack(expand=True, fill="both")

        self._construir_seccion_archivo(contenedor)
        self._construir_barra_acciones(contenedor)
        self._construir_visor_contenido(contenedor)
        self._construir_consola_estado(contenedor)

    def _construir_seccion_archivo(self, parent: ttk.Frame):
        frame_ruta = ttk.LabelFrame(parent, text="1. Origen del archivo", padding=10)
        frame_ruta.pack(fill="x", pady=(0, 8))
        frame_ruta.columnconfigure(1, weight=1)

        ttk.Label(frame_ruta, text="Archivo / Ruta:").grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.ent_ruta = ttk.Entry(frame_ruta, font=("Consolas", 10))
        self.ent_ruta.insert(0, "prueba.txt")
        self.ent_ruta.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        self.ent_ruta.bind("<Return>", lambda _: self._procesar_archivo(mayusculas=False))

        ttk.Button(
            frame_ruta, text="Examinar...", width=12, command=self._seleccionar_archivo
        ).grid(row=0, column=2, sticky="e")

    def _construir_barra_acciones(self, parent: ttk.Frame):
        frame_acciones = ttk.Frame(parent)
        frame_acciones.pack(fill="x", pady=(0, 8))

        ttk.Button(
            frame_acciones, text="Leer contenido original",
            command=lambda: self._procesar_archivo(mayusculas=False)
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        ttk.Button(
            frame_acciones, text="Leer en mayúsculas",
            command=lambda: self._procesar_archivo(mayusculas=True)
        ).pack(side="left", expand=True, fill="x", padx=4)

        self.btn_copiar = ttk.Button(
            frame_acciones, text="Copiar", width=10, state="disabled",
            command=self._copiar_contenido
        )
        self.btn_copiar.pack(side="left", padx=4)

        ttk.Button(
            frame_acciones, text="Limpiar", width=10, command=self._limpiar_visor
        ).pack(side="right", padx=(4, 0))

    def _construir_visor_contenido(self, parent: ttk.Frame):
        frame_visor = ttk.LabelFrame(parent, text="2. Contenido (UTF-8)", padding=8)
        frame_visor.pack(expand=True, fill="both", pady=(0, 8))

        scrollbar_y = ttk.Scrollbar(frame_visor, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        self.txt_contenido = tk.Text(
            frame_visor, wrap="word", font=("Consolas", 10),
            state="disabled", yscrollcommand=scrollbar_y.set, padx=8, pady=8
        )
        self.txt_contenido.pack(expand=True, fill="both")
        scrollbar_y.config(command=self.txt_contenido.yview)

    def _construir_consola_estado(self, parent: ttk.Frame):
        frame_estado = ttk.LabelFrame(parent, text="Estado / errores", padding=8)
        frame_estado.pack(fill="x")

        self.var_estado = tk.StringVar(value="Seleccione un archivo o presione 'Leer contenido original'.")
        self.lbl_estado = ttk.Label(
            frame_estado, textvariable=self.var_estado,
            font=("Segoe UI", 9, "bold"), foreground="#333333", wraplength=590
        )
        self.lbl_estado.pack(anchor="w")

    # helpers

    def _establecer_texto_visor(self, texto: str):
        self.txt_contenido.configure(state="normal")
        self.txt_contenido.delete("1.0", tk.END)
        if texto:
            self.txt_contenido.insert("1.0", texto)
        self.txt_contenido.configure(state="disabled")

    def _notificar(self, mensaje: str, es_error: bool = False):
        color = "#c82333" if es_error else "#1e7e34"
        prefijo = "✖ " if es_error else "✔ "
        self.lbl_estado.configure(foreground=color)
        self.var_estado.set(f"{prefijo}{mensaje}")

    def _seleccionar_archivo(self):
        directorio_base = Path(__file__).resolve().parent
        ruta_elegida = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            initialdir=directorio_base,
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Scripts Python", "*.py"),
                ("Todos los archivos", "*.*"),
            ]
        )
        if ruta_elegida:
            self.ent_ruta.delete(0, tk.END)
            self.ent_ruta.insert(0, ruta_elegida)
            self._procesar_archivo(mayusculas=False)

    def _procesar_archivo(self, mayusculas: bool):
        try:
            ruta_ingresada = self.ent_ruta.get()
            lector = LeerArchivo(ruta_ingresada)

            contenido = lector.leer_en_mayusculas() if mayusculas else lector.leer_contenido()
            self._texto_actual = contenido

            if contenido:
                self._establecer_texto_visor(contenido)
                self.btn_copiar.configure(state="normal")
                num_lineas = contenido.count("\n") + 1
                modo = "mayúsculas" if mayusculas else "original"
                self._notificar(
                    f"[{modo}] '{lector.ruta.name}': {num_lineas} líneas, {len(contenido)} caracteres."
                )
            else:
                self._establecer_texto_visor("[archivo vacío]")
                self.btn_copiar.configure(state="disabled")
                self._notificar(f"'{lector.ruta.name}' abierto, pero está vacío.")

        except (ValueError, FileNotFoundError, IsADirectoryError, PermissionError, ErrorLecturaArchivo) as error:
            self._texto_actual = ""
            self._establecer_texto_visor("")
            self.btn_copiar.configure(state="disabled")
            self._notificar(str(error), es_error=True)

    def _copiar_contenido(self):
        if not self._texto_actual:
            return
        self.raiz.clipboard_clear()
        self.raiz.clipboard_append(self._texto_actual)
        self._notificar("Contenido copiado al portapapeles.")

    def _limpiar_visor(self):
        self._texto_actual = ""
        self._establecer_texto_visor("")
        self.btn_copiar.configure(state="disabled")
        self.lbl_estado.configure(foreground="#333333")
        self.var_estado.set("Visor limpio.")
        self.ent_ruta.focus_set()


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AppLectorArchivoGUI(raiz)
    raiz.mainloop()