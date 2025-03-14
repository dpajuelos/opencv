import cv2
import face_recognition
import os
import time

base_folder = 'rostros_registrados'
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("⚠️ Error: No se pudo acceder a la cámara.")
    exit()

print("✅ Presiona 's' para comenzar el registro de una persona.")
print("✅ Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Error: No se pudo capturar la imagen.")
        break

    cv2.imshow('Registro de Rostros', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        nombre = input("🔹 Ingresa el nombre de la persona: ").strip()
        if not nombre:
            print("⚠️ Error: Nombre vacío. Inténtalo de nuevo.")
            continue

        person_folder = os.path.join(base_folder, nombre)
        os.makedirs(person_folder, exist_ok=True)

        print(f"📸 Capturando imágenes para {nombre}... Mueve el rostro para diferentes ángulos.")
        time.sleep(2)  

        count = 0
        max_images = 10  

        while count < max_images:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Error: No se pudo capturar la imagen.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)

            if face_locations:
                top, right, bottom, left = face_locations[0]
                face_image = frame[top:bottom, left:right]

                img_path = os.path.join(person_folder, f"{nombre}_{count}.jpg")
                cv2.imwrite(img_path, face_image)
                print(f"✅ Imagen {count + 1}/{max_images} guardada.")

                count += 1
                time.sleep(0.5)  

            cv2.imshow('Registro de Rostros', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print(f"🎉 Registro de {nombre} completado con {count} imágenes.")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("✅ Registro finalizado.")
