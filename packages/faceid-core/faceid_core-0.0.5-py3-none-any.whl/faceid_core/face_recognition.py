import cv2
import insightface
import numpy as np
from pathlib import Path
from sklearn import preprocessing
from faceid_core.deploy_configuration import DeployConfig


class FaceRecognition:
    def __init__(self, conf_file):
        self.config = DeployConfig(conf_file)
        self.model = insightface.app.FaceAnalysis()
        self.model.prepare(ctx_id=self.config.gpu_id, det_size=(640, 640))
        self.faces_embedding = list()
        #
        self.load_faces(self.config.face_db)

    #
    def load_faces(self, face_db_path):
        if not Path(face_db_path).exists():
            Path.mkdir(face_db_path)

        face_db_path = Path(face_db_path)  # преобразуем строку в объект Path
        for path in face_db_path.rglob("*"):  # используем .rglob() для рекурсивного обхода всех файлов
            if path.is_file():  # проверяем, что path является файлом
                input_image = cv2.imdecode(np.fromfile(path, dtype=np.uint8),
                                           1)
                user_id = path.stem
                print("Loader face: % s" % user_id)
                face = self.model.get(input_image)[0]
                embedding = np.array(face.embedding).reshape((1, -1))
                embedding = preprocessing.normalize(embedding)
                self.faces_embedding.append({
                    "user_id": user_id,
                    "feature": embedding
                })

    def register(self, image):
        faces = self.model.get(image)
        if len(faces) != 1:
            print("No face, no registration")
            return None
        # Judging whether the face exists
        embedding = np.array(faces[0].embedding).reshape((1, -1))
        embedding = preprocessing.normalize(embedding)
        is_exits = False
        for com_face in self.faces_embedding:
            r = self.feature_compare(embedding, com_face["feature"], self.config.threshold)
            if r:
                is_exits = True
        if is_exits:
            print("The face already exists, no registration")
            return None
        users_id = [d["user_id"] for d in self.faces_embedding]

        if len(users_id) == 0:
            user_id = 0
        else:
            user_id = int(users_id[-1]) + 1

        cv2.imencode('.jpg', image)[1].tofile(Path.joinpath(self.config.face_db, '%s.jpg' % user_id))
        self.faces_embedding.append({
            "user_id": user_id,
            "feature": embedding
        })
        return user_id

    def recognition(self, image):
        faces = self.model.get(image)
        results = list()
        for face in faces:
            result = dict()
            # Start face recognition
            embedding = np.array(face.embedding).reshape((1, -1))
            embedding = preprocessing.normalize(embedding)
            result["user_id"] = "unknown"
            for com_face in self.faces_embedding:
                is_similar = self.feature_compare(embedding, com_face["feature"], self.config.threshold)
                if is_similar:
                    return is_similar
                result["user_id"] = com_face["user_id"] if not is_similar else is_similar
            results.append(result)
        return is_similar

    @staticmethod
    def feature_compare(feature1, feature2, threshold):
        diff = np.subtract(feature1, feature2)
        dist = np.sum(np.square(diff), 1)
        print("Human Face European Distance:% F" % dist)
        if dist < threshold:
            return True
        else:
            return False
