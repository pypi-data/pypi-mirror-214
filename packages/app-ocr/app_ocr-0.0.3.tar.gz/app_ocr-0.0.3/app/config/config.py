"""

Config Model Path

"""

import yaml
import cv2
import io
import numpy as np
import base64
from fastapi import HTTPException
from logger import setup_logger
logging = setup_logger(__name__)


RECOGNITION_INIT = 0.2


def load_face_id_model():
    face_id_config = read_from_config(file_yml='app/config/just_scan_ai.yaml')

    face_id = face_id_config['model_just_scan_structures']['face_id_model']

    retinaface = face_id['retinaface']
    arcface = face_id['arcface']
    return retinaface, arcface


def read_from_config(file_yml):
    with open(file_yml, encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config


def process_input_b64(image_b64: base64):
    try:
        return base64.b64decode(image_b64)
    except:
        logging.error(f'error at running {process_input_b64.__name__}, invalid image format')
        raise HTTPException(status_code=400,
                            detail={'status': 400, 'code': 'INVALID_IMAGE_FORMAT',
                                    'error': 'invalid image format'})


def process_input(file: bytes) -> np.array:
    return np.asarray(bytearray(io.BytesIO(file).read()), dtype=np.uint8)


def processing_image(file: str) -> np.array:
    return cv2.imdecode(process_input(process_input_b64(file)), cv2.IMREAD_COLOR)



