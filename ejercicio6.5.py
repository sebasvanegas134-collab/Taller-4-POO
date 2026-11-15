import tkinter as tk
from tkinter import ttk, messagebox

class SimboloNuloError(Exception):
    pass

class SimboloInexistenteError(Exception):
    pass

class Vendedor:
    def __init__(self, nombres: str, apellidos: str, edad: int):
    
        if not isinstance(edad, int):
            raise TypeError("El parámetro de edad debe ser numérico.")
            
        self.verificar_edad(edad)
        
        self.nombres = nombres
        self.apellidos = apellidos
        self.edad = edad
        
    def verificar_edad(self, edad: int):
        
        if edad < 0 or edad > 120:
            raise ValueError("La edad no puede ser negativa ni mayor a 120.")
        if edad < 18:
            raise ValueError("El vendedor debe ser mayor de 18 años.")
    
    def imprimir(self):
        print(f"{self.nombres} {self.apellidos} - Edad: {self.edad}")


class TablaASCII:
    def __init__(self):
        self.tabla = {}
        
    def setter(self, simbolo: str, numero: int) -> None:
        if not simbolo:
            raise SimboloNuloError("El símbolo no puede ser nulo o vacío.")
        
        if not isinstance(numero, int):
            raise TypeError("El valor debe ser un número entero.")
        self.tabla[simbolo] = numero
        
    def getter(self, simbolo: str) -> int:
        if not simbolo:
            raise SimboloNuloError("El símbolo no puede ser nulo o vacío.")
        if simbolo not in self.tabla:
            raise SimboloInexistenteError(f"El símbolo '{simbolo}' no tiene un valor asociado.")
        return self.tabla[simbolo]


class AppGUI:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Gestor de Excepciones")
        self.raiz.geometry("450x380")
        
        self.backend_ascii = TablaASCII()
        
        self.notebook = ttk.Notebook(self.raiz)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab_vendedor = ttk.Frame(self.notebook)
        self.tab_ascii = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_vendedor, text="Clase Vendedor")
        
        self.notebook.add(self.tab_ascii, text="Tabla ASCII") 
        
        self._construir_tab_vendedor()
        self._construir_tab_ascii()
    
    def _construir_tab_vendedor(self):
        ttk.Label(self.tab_vendedor, text="Nombres:").pack(pady=(15,2))
        self.ent_nombres = ttk.Entry(self.tab_vendedor, width=30)
        self.ent_nombres.pack()
        
        ttk.Label(self.tab_vendedor, text="Apellidos:").pack(pady=(10,2))
        self.ent_apellidos = ttk.Entry(self.tab_vendedor,width=30)
        self.ent_apellidos.pack()
        
        ttk.Label(self.tab_vendedor, text="Edad (Entero):").pack(pady=(10,2))
        self.ent_edad = ttk.Entry(self.tab_vendedor, width=30)
        self.ent_edad.pack()
        
        ttk.Button(self.tab_vendedor,text="Agregar vendedor", command=self.ejecutar_vendedor).pack(pady=20)
        
    def _construir_tab_ascii(self):
        #SETTER
        ttk.Label(self.tab_ascii, text="Guardar Símbolo", font=("", 10, "bold")).pack(pady=(15,5))
        
        frame_set = ttk.Frame(self.tab_ascii)
        frame_set.pack()
        
        ttk.Label(frame_set, text="Símbolo:").grid(row=0, column=0, padx=5)
        self.ent_simbolo_set = ttk.Entry(frame_set, width=10)
        self.ent_simbolo_set.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_set, text="Número:").grid(row=0, column=2, padx=5)
        self.ent_numero_set = ttk.Entry(frame_set, width=10)
        self.ent_numero_set.grid(row=0, column=3, padx=5)
        
        ttk.Button(self.tab_ascii, text="Guardar en Diccionario", command=self.ejecutar_set_ascii).pack(pady=10)
        #GETTER
        ttk.Label(self.tab_ascii, text="Buscar Símbolo", font=("", 10, "bold")).pack(pady=(20,5))
        
        frame_get = ttk.Frame(self.tab_ascii)
        frame_get.pack()
        
        ttk.Label(frame_get, text="Símbolo:").grid(row=0, column=0, padx=5)
        self.ent_simbolo_get = ttk.Entry(frame_get, width=10)
        self.ent_simbolo_get.grid(row=0, column=1, padx=5)
        
        ttk.Button(self.tab_ascii, text="Buscar Valor", command=self.ejecutar_get_ascii).pack(pady=10)
    
    def ejecutar_vendedor(self):
        try:
            nom = self.ent_nombres.get().strip() 
            ape = self.ent_apellidos.get().strip()
            edad_texto = self.ent_edad.get().strip()
            
            
            if not nom or not ape:
                raise ValueError("Los nombres y apellidos no pueden estar vacíos.")
                
            
            try:
                edad_int = int(edad_texto)
            except ValueError:
                raise TypeError("La edad debe ser un número entero válido.")
                
            vendedor = Vendedor(nom, ape, edad_int)
            vendedor.imprimir() 
            
            messagebox.showinfo("Éxito", f"Objeto creado en memoria.\nVendedor: {vendedor.nombres} {vendedor.apellidos}")
            
            
            self.ent_nombres.delete(0, tk.END)
            self.ent_apellidos.delete(0, tk.END)
            self.ent_edad.delete(0, tk.END)
            
        except (ValueError, TypeError) as error:
           
            messagebox.showerror("Error de creación", str(error))

    def ejecutar_set_ascii(self):
        try: 
            simbolo = self.ent_simbolo_set.get().strip()
            num_texto = self.ent_numero_set.get().strip()
            
           
            try:
                num_int = int(num_texto)
            except ValueError:
                raise TypeError("El valor a guardar debe ser un número entero.")
                
            self.backend_ascii.setter(simbolo, num_int)
            messagebox.showinfo("Guardado", f"Símbolo '{simbolo}' asociado al número {num_int}.")
            
            
            self.ent_simbolo_set.delete(0, tk.END)
            self.ent_numero_set.delete(0, tk.END)
            
        except (SimboloNuloError, TypeError) as error:
            messagebox.showerror("Error al Guardar", str(error))

    def ejecutar_get_ascii(self):
        try:
            simbolo = self.ent_simbolo_get.get().strip()
            
            resultado = self.backend_ascii.getter(simbolo)
            messagebox.showinfo("Resultado", f"El valor de '{simbolo}' es: {resultado}")
            
            self.ent_simbolo_get.delete(0, tk.END)

        except (SimboloNuloError, SimboloInexistenteError) as error:
            messagebox.showerror("Error de Búsqueda", str(error))

if __name__ == "__main__":
    raiz = tk.Tk()
    app = AppGUI(raiz)
    raiz.mainloop()