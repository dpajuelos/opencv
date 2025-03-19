# 📸 Reconocimiento Facial con OpenCV y Face\_Recognition

Sistema que permite registrar y reconocer rostros utilizando OpenCV y la librería Face\_Recognition en Python. Captura y almacena múltiples imágenes por persona para mejorar la precisión del reconocimiento.

---

## 🚀 Instalación y Configuración

### 🛠 Dependencias Requeridas

Para que el proyecto funcione correctamente, es necesario instalar:

1. **Python** (versión 3.8 o superior)
2. **Visual Studio Build Tools** con:
   - C++ CMake tools for Windows
   - Windows 10 SDK
   - MSVC v142
3. **CMake** (instalación manual, ver sección abajo)
4. **Dlib** (para procesamiento de rostros)
5. **Face\_Recognition** y **OpenCV**

### 📥 Instalación de Dependencias en Windows

Ejecuta los siguientes comandos en la terminal de Windows (PowerShell o CMD):

```sh
pip install opencv-python
pip install dlib
pip install face_recognition
```

Si tienes problemas con `dlib`, asegúrate de tener las dependencias de Visual Studio correctamente instaladas.

### 🏗 Instalación Manual de CMake en Windows

Si `cmake` no está instalado correctamente o no es detectado, sigue estos pasos:

1. Descarga CMake desde su [sitio oficial](https://cmake.org/download/).
2. Instala CMake y selecciona la opción **"Add CMake to system PATH"** durante la instalación.
3. Verifica la instalación ejecutando en CMD:
   ```sh
   cmake --version
   ```
   Debe mostrar la versión instalada de CMake.

---

## 📌 Uso del Proyecto

### 👤 Registro de Rostros

Ejecuta el script `registro.py` para registrar rostros:

```sh
python registro.py
```

Sigue las instrucciones en pantalla y presiona `S` para registrar un rostro.

### 🔍 Reconocimiento Facial

Ejecuta el script `reconocimiento.py`:

```sh
python reconocimiento.py
```

La cámara detectará rostros y mostrará el nombre de la persona debajo de su rostro.

---

## 📝 Notas Adicionales

- Asegúrate de tener una buena iluminación para mejorar la detección de rostros.
- Se recomienda capturar varias imágenes de cada persona desde diferentes ángulos.
- Para agregar nuevos usuarios, simplemente ejecuta el script de registro y guarda múltiples imágenes.

---

🎯 **Hecho con ❤️**

