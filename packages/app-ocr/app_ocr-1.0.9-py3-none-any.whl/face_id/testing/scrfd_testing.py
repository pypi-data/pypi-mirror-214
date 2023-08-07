from app.face_id.commons.ScrFd.scrfd import SCRFD
from app.face_id.tools.modules import get_image
from app.face_id.commons.ArcFace.ArcFace_onnx import ArcFaceONNX

detector = SCRFD('../modeling/scrfd_model/det_10g.onnx')
detector.prepare(0)


def analyze_facial(img_path):
    img = get_image(img_path)
    bbox, kps = detector.autodetect(img)
    for coor in bbox:
        x1 = int(coor[0])
        y1 = int(coor[1])
        x2 = int(coor[2])
        y2 = int(coor[3])
        face = img[y1:y2, x1:x2]
    return face, kps


rec = ArcFaceONNX()
# img1 = cv2.imread('test_data/d615314455af8cf1d5be.jpg')
# img2 = cv2.imread('test_data/disaster-girl.jpg')

face1, kps1 = analyze_facial(img_path='../../../test_data/d615314455af8cf1d5be.jpg')
print(kps1)
face2, kps2 = analyze_facial(img_path='../../../test_data/img.png')
print(kps2)
embedding1 = rec.get(face1, kps1[0])
embedding2 = rec.get(face2, kps2[0])
sim = rec.compute_sim(embedding1, embedding2)
print(sim)