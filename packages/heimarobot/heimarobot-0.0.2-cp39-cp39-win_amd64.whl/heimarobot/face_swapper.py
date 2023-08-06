import insightface
from face_detection import FaceDetection
from insightface.app.common import Face
from face_recognition import FaceRecognition

class FaceSwapper:

    def __init__(self):
        self.recognition = FaceRecognition()
        self.model = insightface.model_zoo.get_model('best-swapper.onnx', download=False, download_zip=False)


    def get_source_face(self,sourceImg):
        
        return self.recognition.predict(sourceImg)[0]

    def predict(self,sourceFace,targetImg):
        """
            source: 参考的脸
            target: 被替换的脸
        """
        targetFace = self.recognition.predict(targetImg)[0]

        dst = None
        if sourceFace and targetFace:
            dstImg = targetImg.copy()
            dst = self.model.get(dstImg, targetFace, sourceFace, paste_back=True)  
        return dst
    
    def compute_sim(self,feature1,feature2):
        return self.model.compute_sim(feature1[0].embedding,feature2[0].embedding)