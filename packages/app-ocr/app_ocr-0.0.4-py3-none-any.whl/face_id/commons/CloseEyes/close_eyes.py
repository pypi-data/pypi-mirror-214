import onnxruntime
import onnx
import numpy as np
import cv2
from app.face_id.commons.CloseEyes.utils import extract_eye


class CloseEyes:
    def __init__(self, model_file='app/face_id/modeling/close_eyes_model/oce.onnx', session=None):
        assert model_file is not None
        self.model_file = model_file
        self.session = session
        self.taskname = 'recognition'
        find_sub = False
        find_mul = False
        model = onnx.load(self.model_file)
        graph = model.graph
        for nid, node in enumerate(graph.node[:8]):
            # print(nid, node.name)
            if node.name.startswith('Sub') or node.name.startswith('_minus'):
                find_sub = True
            if node.name.startswith('Mul') or node.name.startswith('_mul'):
                find_mul = True
        if find_sub and find_mul:
            # mxnet arcface model
            input_mean = 0.0
            input_std = 1.0
        else:
            input_mean = 127
            input_std = 127
        self.input_mean = input_mean
        self.input_std = input_std
        # print('input mean and std:', self.input_mean, self.input_std)
        if self.session is None:
            self.session = onnxruntime.InferenceSession(
                self.model_file, providers=['CPUExecutionProvider'])
        input_cfg = self.session.get_inputs()[0]
        input_shape = input_cfg.shape
        input_name = input_cfg.name
        self.input_size = tuple(input_shape[2:4][::-1])
        self.input_shape = input_shape
        outputs = self.session.get_outputs()
        output_names = []
        for out in outputs:
            output_names.append(out.name)
        self.input_name = input_name
        self.output_names = output_names
        assert len(self.output_names) == 1
        self.output_shape = outputs[0].shape

    def prepare(self, ctx_id, **kwargs):
        if ctx_id < 0:
            self.session.set_providers(['CPUExecutionProvider'])

    def crop_eye(self, image, left_eye, right_eye):
        left_eyes, right_eyes = extract_eye(image, left_eye, right_eye)
        return left_eyes, right_eyes

    def predict(self, img):
        net = self.get(img)
        ids = np.argmax(net)
        confidence = np.max(net)
        ids = True if ids == 0 else False
        # 0: closed, 1: open
        return ids, confidence

    def get(self, img):
        return self.get_feat(img)

    # mean = (104, 117, 123)
    def get_feat(self, imgs):
        if not isinstance(imgs, list):
            imgs = [imgs]
        input_size = self.input_size
        input_blob = cv2.dnn.blobFromImages(imgs, scalefactor=1.0 / 255, size=input_size, mean=(104, 117, 123), swapRB=True,
                                            crop=False)
        # input_blob /= 255.
        net_out = self.session.run(
            self.output_names, {self.input_name: input_blob})[0]
        return net_out

    # def forward(self, batch_data):
    #     blob = (batch_data - self.input_mean) / self.input_std
    #     net_out = self.session.run(self.output_names, {self.input_name: blob})[0]
    #     return net_out
