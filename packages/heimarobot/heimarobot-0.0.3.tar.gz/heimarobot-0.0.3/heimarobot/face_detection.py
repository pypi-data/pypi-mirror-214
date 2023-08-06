import heimarobot.insightface as insightface
from heimarobot.insightface.app.common import Face

class FaceDetection:
    def __init__(self):
        self.model = insightface.model_zoo.get_model('best-detect.onnx', download=False, download_zip=False)
        self.model.prepare(0, input_size=(640, 640), det_thresh=0.5)

    def predict(self,src,max_num=0):
        # 获取检测人脸特征
        bboxes, kpss = self.model.detect(src, max_num=max_num)

        if bboxes.shape[0] == 0:
            return []
        faces = []
        for i in range(bboxes.shape[0]):
            bbox = bboxes[i, 0:4]
            det_score = bboxes[i, 4]
            kps = None
            if kpss is not None:
                kps = kpss[i]
            face = Face(bbox=bbox, kps=kps, det_score=det_score)
            faces.append(face)

        return faces


