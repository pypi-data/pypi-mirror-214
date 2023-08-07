from ..modules.corner_detection.id_card_aligment import align_image
from ..commons.config import Config
from ..modules.mrc.utils import mrc_crop_model, mrc_detect_model
from ..modules.passport.passport_detection import passport_detect_model

classify, crop, front_side, back_side = Config().load_all_models()


class MergeIdCardModel(object):
    def __init__(self):
        pass

    @staticmethod
    def detect_corner(image, mrc=False):
        if mrc:
            detection_boxes, detection_scores, detection_classes = mrc_crop_model.detect_objects(image)
            return align_image(image, detection_boxes, mrc_crop_model.get_label())
        else:
            detection_boxes, detection_scores, detection_classes = crop.detect_objects(
                image)
            return align_image(image, detection_boxes, crop.get_label())

    @staticmethod
    def recognize_fe(image, mrc=False, passport=False):
        if mrc:
            detection_boxes, detection_score, detection_classes = mrc_detect_model.detect_objects(image)
            return mrc_detect_model.get_label(), detection_boxes
        elif passport:
            detection_boxes, detection_score, detection_classes = passport_detect_model.detect_objects(image)
            return passport_detect_model.get_label(), detection_boxes
        else:
            detection_boxes, detection_score, detection_classes = front_side.detect_objects(image)
            return front_side.get_label(), detection_boxes

    @staticmethod
    def recognize_be(image):
        detection_boxes, detection_score, detection_classes = back_side.detect_objects(image)
        return back_side.get_label(), detection_boxes

    @staticmethod
    def classify_card(image):
        return classify.predict(image)
