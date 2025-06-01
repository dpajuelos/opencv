import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import face_recognition
import os
import time

# === Carpeta para guardar rostros ===
base_folder = 'rostros_registrados'
os.makedirs(base_folder, exist_ok=True)

# === Configuración de cámara ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("⚠️ No se pudo acceder a la cámara.")

# === Ventana principal ===
root = tk.Tk()
root.title("Registro de Rostros")
root.geometry("800x600")

# === Widgets ===
video_label = tk.Label(root)
video_label.pack()

entry_label = tk.Label(root, text="Nombre:", font=("Arial", 12))
entry_label.pack()

name_entry = tk.Entry(root, font=("Arial", 12), width=30)
name_entry.pack(pady=5)

status_label = tk.Label(root, text="", font=("Arial", 11), fg="green")
status_label.pack()

btn_registrar = tk.Button(root, text="Iniciar Registro", font=("Arial", 12), bg="blue", fg="white")
btn_registrar.pack(pady=10)

btn_salir = tk.Button(root, text="Salir", command=lambda: cerrar(), font=("Arial", 12), bg="red", fg="white")
btn_salir.pack()

capturando = False
contador = 0
max_imagenes = 10
nombre = ""

def mostrar_video():
    global capturando, contador, nombre

    ret, frame = cap.read()
    if not ret:
        root.after(10, mostrar_video)
        return

    # Mostrar video
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if capturando:
        small_frame = cv2.resize(frame_rgb, (0, 0), fx=0.5, fy=0.5)
        face_locations = face_recognition.face_locations(small_frame)

        if face_locations:
            top, right, bottom, left = [v * 2 for v in face_locations[0]]  # reescalar
            face_image = frame[top:bottom, left:right]

            person_folder = os.path.join(base_folder, nombre)
            os.makedirs(person_folder, exist_ok=True)
            img_path = os.path.join(person_folder, f"{nombre}_{contador}.jpg")
            cv2.imwrite(img_path, face_image)
            contador += 1
            status_label.config(text=f"✅ Imagen {contador}/{max_imagenes} guardada.")

            # Dibujar rectángulo en el frame
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            if contador >= max_imagenes:
                capturando = False
                status_label.config(text=f"🎉 Registro de {nombre} completado.")
        else:
            status_label.config(text="❌ Rostro no detectado. Intenta mirar a la cámara.")

    # Convertir a imagen para Tkinter
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    root.after(10, mostrar_video)

def iniciar_registro():
    global capturando, contador, nombre

    nombre = name_entry.get().strip()
    if not nombre:
        messagebox.showwarning("Nombre vacío", "⚠️ Por favor, ingresa un nombre.")
        return

    contador = 0
    capturando = True
    status_label.config(text=f"📸 Registrando rostro de {nombre}...")

def cerrar():
    cap.release()
    root.destroy()

btn_registrar.config(command=iniciar_registro)

# Iniciar video
mostrar_video()
root.mainloop()
