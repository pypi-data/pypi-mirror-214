import heimarobot.insightface as insightface
from .face_detection import FaceDetection
from heimarobot.insightface.app.common import Face

class FaceRecognition:

    def __init__(self):
        self.detector = FaceDetection()

        self.model = insightface.model_zoo.get_model('best-recognition.onnx', download=False, download_zip=False)
        self.model.prepare(0)



    def predict(self,src):
        faces = self.detector.predict(src)

        for face in faces:
            self.model.get(src, face)

        # if bboxes.shape[0] == 0:
        #     return []
        # ret = []
        # for i in range(bboxes.shape[0]):
        #     bbox = bboxes[i, 0:4]
        #     det_score = bboxes[i, 4]
        #     kps = None
        #     if kpss is not None:
        #         kps = kpss[i]
        #     face = Face(bbox=bbox, kps=kps, det_score=det_score)
        #     self.model.get(src, face)
        #     ret.append(face)
        return faces
    
    def compute_sim(self,feature1,feature2):
        return self.model.compute_sim(feature1[0].embedding,feature2[0].embedding)