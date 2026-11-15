import tkinter as tk
from tkinter import messagebox

# --- A. Excepciones Personalizadas para simular los errores de Java ---
class ExcepcionNula(Exception):
    pass

class ExcepcionFueraDeRango(Exception):
    pass

class Procesado:
    def __init__(self, modo):
        self.modo = modo

    def operacion(self):
        if self.modo == "bloque1":
            try:
                print("Ingresando al primer try")
                
                cociente = 10000 / 0 
                print("Después de la división") 
            except ZeroDivisionError:
                print("División por cero")
                return "Impreso en consola:\nIngresando al primer try\nDivisión por cero\nIngresando al primer finally"
            finally:
                print("Ingresando al primer finally")

        elif self.modo == "bloque2":
            try:
                print("Ingresando al segundo try")
                objeto = None
               
                objeto.to_string() 
                print("Imprimiendo objeto")
            except AttributeError:
                print("Ocurrió una excepción")
                return "Impreso en consola:\nIngresando al segundo try\nOcurrió una excepción\nIngresando al segundo finally"
            finally:
                print("Ingresando al segundo finally")

        elif self.modo == "bloque3":
            try:
                print("Ingresando al try del bloque 3")
               
                numero = int("Número") 
                print(numero) #
            except ValueError:
                print("Excepción de formato de número")
                return "Impreso en consola:\nIngresando al try del bloque 3\nExcepción de formato de número\nIngresando al finally"
            finally:
                print("Ingresando al finally")

        elif self.modo == "bloque4":
            try:
                print("Ingresando al try del bloque 4")
                
                texto = "Programación"
                caracter = texto[12] 
                print(caracter) 
            except IndexError:
                print("Índice de string por fuera del límite")
                return "Impreso en consola:\nIngresando al try del bloque 4\nÍndice de string por fuera del límite"
            finally:
                pass 


class GUI:
    def __init__(self, ventana: tk.Tk):
        self.ventana = ventana
        self.ventana.title("Manejo de errores ")
        self.ventana.geometry("550x400")
        
        
        tk.Label(self.ventana, text="Selecciona un bloque de código para ejecutar:", font=("Arial", 11, "bold")).pack(pady=15)
        
        
        self.btn_bloque1 = tk.Button(self.ventana, text="Bloque 1: División por Cero", width=40, command=lambda: self.ExeCalculo("bloque1"))
        self.btn_bloque1.pack(pady=5)
        
        self.btn_bloque2 = tk.Button(self.ventana, text="Bloque 2: Objeto Nulo (NullPointer)", width=40, command=lambda: self.ExeCalculo("bloque2"))
        self.btn_bloque2.pack(pady=5)
        
        self.btn_bloque3 = tk.Button(self.ventana, text="Bloque 3: Formato de Número", width=40, command=lambda: self.ExeCalculo("bloque3"))
        self.btn_bloque3.pack(pady=5)

        self.btn_bloque4 = tk.Button(self.ventana, text="Bloque 4: Índice de String", width=40, command=lambda: self.ExeCalculo("bloque4"))
        self.btn_bloque4.pack(pady=5)

        
        self.lbl_resultado = tk.Label(self.ventana, text="", justify=tk.LEFT, fg="blue")
        self.lbl_resultado.pack(pady=20)

    def ExeCalculo(self, modo):
        
        self.lbl_resultado.config(text="Revisa la consola para ver el flujo exacto...")
        
        try:
            instancia = Procesado(modo)
            resultado = instancia.operacion()
            
            
            if resultado:
                self.lbl_resultado.config(text=resultado)
                messagebox.showinfo("Ejecución Exitosa", f"El bloque se ejecutó.\n\nRevisa la consola y la ventana principal.")
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))
        finally: 
            print("[GUI] Ejercicio finalizado. Esperando siguiente instrucción.\n" + "-"*30)

if __name__ == "__main__":
    raiz = tk.Tk()
    app = GUI(raiz)
    raiz.mainloop()