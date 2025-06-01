import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import face_recognition
import numpy as np
import os

# === Cargar rostros registrados ===
base_folder = "rostros_registrados"
known_face_encodings = []
known_face_names = []

for person_name in os.listdir(base_folder):
    person_folder = os.path.join(base_folder, person_name)
    if os.path.isdir(person_folder):
        for image_name in os.listdir(person_folder):
            image_path = os.path.join(person_folder, image_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(person_name)

# === Interfaz Tkinter ===
root = tk.Tk()
root.title("Reconocimiento Facial en Tiempo Real")
root.geometry("800x600")

# Label para video
video_label = tk.Label(root)
video_label.pack()

# Inicializar cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    messagebox.showerror("Error", "⚠️ No se pudo acceder a la cámara.")
    root.destroy()

def mostrar_video():
    ret, frame = cap.read()
    if not ret:
        root.after(10, mostrar_video)
        return

    # Procesar frame para reconocimiento
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.5, fy=0.5)
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Desconocido"

        if True in matches:
            match_indexes = [i for i, match in enumerate(matches) if match]
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = match_indexes[np.argmin([face_distances[i] for i in match_indexes])]
            name = known_face_names[best_match_index]

        # Escalar posiciones
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom), (right, bottom + 20), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Convertir frame para Tkinter
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    # Repetir
    root.after(10, mostrar_video)

# Cerrar aplicación
def cerrar_app():
    cap.release()
    root.destroy()

# Botón para salir
btn_salir = tk.Button(root, text="Salir", command=cerrar_app, bg="red", fg="white", font=("Arial", 12))
btn_salir.pack(pady=10)

# Iniciar video
mostrar_video()

root.mainloop()
