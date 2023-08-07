"""

Config Model Path

"""

import yaml
import cv2
import io
import numpy as np
import base64
from fastapi import HTTPException
from .logger import setup_logger

logging = setup_logger(__name__)

RECOGNITION_INIT = 0.2


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
