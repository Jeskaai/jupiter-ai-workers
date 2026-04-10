# Jupiter Pose Module & Vision Service

Este es un MVP en Python para detectar postura corporal usando `OpenPose` si está disponible y `MediaPipe` como respaldo automático. Además, incluye un servicio aislado (`VisionService`) que procesa imágenes para detectar emociones, contacto visual (Face Mesh) y postura de forma estructurada.

## ¿Qué hace este proyecto?

Este proyecto sirve para detectar y seguir características visuales en tiempo real usando cámara o video.

Sus funcionalidades clave son:
- **Detección de postura:** detectar los puntos clave de los hombros, decidir si la postura de una persona está "abierta" o "cerrada" y calcular la cantidad de movimiento (vía PoseDetector / MediaPipe Pose).
- **Extracción de puntos faciales y emociones (VisionService):** Detectar y estructurar puntos faciales (`face_landmarks`, `face_blendshapes`) para análisis de contacto visual y emociones, utilizando la API Tasks de MediaPipe.

## ¿Por qué usamos OpenPose como opción principal?

`OpenPose` se usa como backend principal para posturas corporales porque funciona muy bien cuando hay varias personas en cámara. Su ventaja es que analiza primero todas las partes del cuerpo que aparecen en la imagen y después las agrupa por persona, rindiendo de forma estable. En cambio, `MediaPipe` procesa cada persona por separado y consume más recursos. Sin embargo, para escenarios estructurados y puntos faciales detallados, la integración de MediaPipe Tasks resulta esencial.

## Archivos principales

- `main.py`: punto de entrada del programa.
- `pose_detector.py`: carga el backend y extrae los puntos de los hombros de manera interactiva.
- `app/services/vision_service.py`: Servicio aislado puro mediante MediaPipe Tasks para extraer facial landmarks (Face Mesh) y pose de un `numpy` frame.
- `tests/test_vision.py`: Script de prueba local para validar que `VisionService` retorna datos robustamente.
- `utils.py`: dibuja información de depuración y exporta el JSON.
- `config.py`: contiene las constantes por defecto.
- `output.json`: archivo de salida generado al ejecutar el proyecto.

## Requisitos

Se recomienda usar Python 3.12 (hasta 3.14 validado para pruebas).

## Instalación

```powershell
uv venv --python 3.12 .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ejecutar con webcam

```powershell
python main.py --source 0
```

## Ejecutar Pruebas Locales (VisionService)

El script de prueba para el módulo independiente de visión:
```powershell
python tests/test_vision.py
```

## Formato de salida JSON

Cada frame se guarda con una estructura como esta:

```json
{
  "frame": 1,
  "people": [
    {
      "id": 0,
      "shoulder_left": [100, 200],
      "shoulder_right": [180, 200],
      "posture": "open",
      "movement_px": 12.4
    }
  ]
}
```

## Nota sobre multipersona

Con `OpenPose`, el diseño ya está pensado para soportar varias personas de forma más eficiente. Con `MediaPipe`, procesamos el enfoque centrado para la detección facial y corporal individual en validaciones del servicio.
