import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Función para ejecutar el script de registro de rostros
def registrar_rostro():
    messagebox.showinfo("Registro", "Se abrirá la cámara para registrar un nuevo rostro.")
    subprocess.run([sys.executable, "registro.py"])

# Función para ejecutar el script de reconocimiento facial
def reconocer_rostro():
    messagebox.showinfo("Reconocimiento", "Se abrirá la cámara para reconocimiento facial.")
    subprocess.run([sys.executable, "reconocimiento.py"])

# Función para salir de la aplicación
def salir():
    if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
        root.destroy()

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Reconocimiento Facial")
root.resizable(False, False)
root.update_idletasks()
width = 400
height = 300
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

# Título
tk.Label(root, text="Bienvenido", font=("Arial", 18, "bold")).pack(pady=20)
tk.Label(root, text="Selecciona una opción:", font=("Arial", 12)).pack(pady=10)

# Botones
tk.Button(root, text="📷 Registrar Rostro", font=("Arial", 12), width=25, command=registrar_rostro).pack(pady=10)
tk.Button(root, text="👁️ Reconocer Rostro", font=("Arial", 12), width=25, command=reconocer_rostro).pack(pady=10)
tk.Button(root, text="❌ Salir", font=("Arial", 12), width=25, command=salir).pack(pady=10)

# Ejecutar la interfaz
root.mainloop()
