"""
Sistema de Reconocimiento Facial en Tiempo Real

Descripción:
    Este script detecta rostros en la cámara web y los compara con una base de datos de rostros registrados
    para identificar personas conocidas.

Uso:
    1. Ejecutar: python reconocimiento_facial.py
    2. Presionar 'q' para salir.

Requisitos:
    - Carpeta 'rostros_registrados' con subcarpetas de personas (cada subcarpeta debe contener imágenes de su rostro).
"""

import cv2
import face_recognition
import os
import numpy as np

# Configuración inicial
base_folder = "rostros_registrados"  # Carpeta base con imágenes de referencia
known_face_encodings = []  # Almacena los embeddings faciales conocidos
known_face_names = []      # Almacena los nombres asociados a los embeddings

# Cargar rostros registrados
for person_name in os.listdir(base_folder):
    person_folder = os.path.join(base_folder, person_name)
    if os.path.isdir(person_folder): 
        for image_name in os.listdir(person_folder):
            image_path = os.path.join(person_folder, image_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:  # Si se detecta un rostro en la imagen
                known_face_encodings.append(encodings[0])
                known_face_names.append(person_name)

# Inicializar cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("⚠️ Error: No se pudo acceder a la cámara.")
    exit()

print("✅ Reconocimiento facial en marcha. Presiona 'q' para salir.")

# Bucle principal
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Error: No se pudo capturar la imagen.")
        break

    # Convertir a RGB (face_recognition usa RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar rostros en el frame
    face_locations = face_recognition.face_locations(rgb_frame)
    if not face_locations:
        cv2.imshow('Reconocimiento Facial', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # Generar embeddings de los rostros detectados
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Comparar con la base de datos
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Desconocido"

        # Encontrar la coincidencia más cercana
        if True in matches:
            match_indexes = [i for i, match in enumerate(matches) if match]
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = match_indexes[np.argmin([face_distances[i] for i in match_indexes])]
            name = known_face_names[best_match_index]

        # Dibujar rectángulo y etiqueta
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom + 20), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Reconocimiento Facial', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
print("✅ Reconocimiento finalizado.")
