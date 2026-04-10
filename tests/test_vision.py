import sys
import os
import cv2
import numpy as np

# Add the root directory to the python path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.vision_service import VisionService

def test_process_frame():
    # Initialize the vision service
    vision_service = VisionService()
    
    # Create a dummy image for testing
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.circle(dummy_frame, (320, 240), 100, (255, 255, 255), -1)
    
    print("Enviando dummy frame al VisionService...")
    try:
        results = vision_service.process_frame(dummy_frame)
        print("Procesamiento exitoso.")
        print(f"Llaves en resultados: {results.keys()}")
        
        assert "face_landmarks" in results
        assert "pose_landmarks" in results
        
        print(f"Face landmarks detectados: {'Sí' if results['face_landmarks'] else 'No'}")
        print(f"Pose landmarks detectados: {'Sí' if results['pose_landmarks'] else 'No'}")
        
    except Exception as e:
        print(f"Error procesando frame: {e}")
        assert False, f"El procesamiento lanzó una excepción: {e}"
    finally:
        vision_service.close()

if __name__ == "__main__":
    test_process_frame()
    print("Prueba completada exitosamente.")
