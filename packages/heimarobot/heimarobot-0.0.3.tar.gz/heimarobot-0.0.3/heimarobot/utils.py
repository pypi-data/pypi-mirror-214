import cv2 as cv
import numpy as np

def draw_faces(img, faces):
    import cv2
    dimg = img.copy()
    for i in range(len(faces)):
        face = faces[i]
        box = face.bbox.astype(int)
        color = (0, 0, 255)
        cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)
        if face.kps is not None:
            kps = face.kps.astype(int)
            #print(landmark.shape)
            for l in range(kps.shape[0]):
                color = (0, 0, 255)
                if l == 0 or l == 3:
                    color = (0, 255, 0)
                cv2.circle(dimg, (kps[l][0], kps[l][1]), 1, color,
                            2)
        if face.gender is not None and face.age is not None:
            cv2.putText(dimg,'%s,%d'%(face.sex,face.age), (box[0]-1, box[1]-4),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),1)

    return dimg

def draw_landmarks(img,faces):
    dimg = img.copy()
    for face in faces:
        landmark = face["landmark_2d_106"]
        lmk = np.round(landmark).astype(np.int32)
        print(lmk.shape)
        for l in range(lmk.shape[0]):
            color = (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255))
            cv.circle(dimg, (lmk[l][0], lmk[l][1]), 1, color,2)
    return dimg
