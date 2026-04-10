import urllib.request
from pathlib import Path
import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode

# URLs to download the models
FACE_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task"
POSE_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task"

class VisionService:
    def __init__(self, model_dir="models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.face_model_path = self.model_dir / "face_landmarker.task"
        self.pose_model_path = self.model_dir / "pose_landmarker_full.task"
        
        self._ensure_models()
        self.face_landmarker = self._setup_face()
        self.pose_landmarker = self._setup_pose()
        
        self.mp_image_format = mp.ImageFormat

    def _ensure_models(self):
        if not self.face_model_path.exists():
            print("Descargando modelo Face Landmarker...")
            urllib.request.urlretrieve(FACE_MODEL_URL, self.face_model_path)
        if not self.pose_model_path.exists():
            print("Descargando modelo Pose Landmarker...")
            urllib.request.urlretrieve(POSE_MODEL_URL, self.pose_model_path)

    def _setup_face(self):
        base_options = BaseOptions(model_asset_path=str(self.face_model_path))
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=VisionTaskRunningMode.IMAGE,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1)
        return vision.FaceLandmarker.create_from_options(options)

    def _setup_pose(self):
        base_options = BaseOptions(model_asset_path=str(self.pose_model_path))
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=VisionTaskRunningMode.IMAGE,
            num_poses=1)
        return vision.PoseLandmarker.create_from_options(options)

    def process_frame(self, frame: np.ndarray):
        """
        Procesa el frame usando MediaPipe Tasks para extraer puntos clave 
        de la cara (emociones, contacto visual) y del cuerpo (postura).
        Retorna un diccionario con los resultados.
        """
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=self.mp_image_format.SRGB, data=rgb_frame)
        
        face_result = self.face_landmarker.detect(mp_image)
        pose_result = self.pose_landmarker.detect(mp_image)
        
        result = {
            "face_landmarks": None,
            "face_blendshapes": None,
            "pose_landmarks": None
        }
        
        if face_result.face_landmarks:
            result["face_landmarks"] = face_result.face_landmarks[0]
        if face_result.face_blendshapes:
            result["face_blendshapes"] = face_result.face_blendshapes[0]
            
        if pose_result.pose_landmarks:
            result["pose_landmarks"] = pose_result.pose_landmarks[0]
            
        return result
        
    def close(self):
        self.face_landmarker.close()
        self.pose_landmarker.close()
