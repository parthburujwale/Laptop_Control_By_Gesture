import joblib
import numpy as np
import pandas as pd



class GestureDetector:


    def __init__(self):

        self.model = joblib.load(
            "gesture_model.pkl"
        )


    def normalize_landmarks(self, landmarks):

        points = np.array(
            [
                [x,y]
                for _,x,y in landmarks
            ]
        )


        points = points - points[0]


        scale = np.linalg.norm(
            points[9]
        )


        if scale != 0:
            points /= scale


        return points



    def extract_features(self, points):

        features = list(
            points.flatten()
        )


        def dist(a,b):

            return np.linalg.norm(
                points[a]-points[b]
            )


        features += [

            dist(4,8),
            dist(4,12),
            dist(4,16),
            dist(4,20),

            dist(8,12),
            dist(12,16),
            dist(16,20)

        ]


        return np.array(features)



    def detect(self, landmarks):

        if not landmarks:
            return "None"


        normalized = self.normalize_landmarks(
            landmarks
        )


        features = self.extract_features(
            normalized
        )


        features_df = pd.DataFrame(
            [features],
            columns=self.model.feature_names_in_
        )


        probabilities = self.model.predict_proba(
            features_df
        )[0]


        confidence = np.max(probabilities)


        prediction = self.model.classes_[
            np.argmax(probabilities)
        ]


        if confidence < 0.75:
            return "Unknown"


        return prediction