import cv2
import mediapipe as mp



class HandTracker:


    def __init__(self):

        self.hands=mp.solutions.hands.Hands(

            max_num_hands=1,

            min_detection_confidence=0.7,

            min_tracking_confidence=0.7

        )


        self.drawer=mp.solutions.drawing_utils



    def get_landmarks(self,frame):


        rgb=cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        results=self.hands.process(rgb)


        landmarks=[]



        if results.multi_hand_landmarks:


            hand=results.multi_hand_landmarks[0]


            for idx,lm in enumerate(hand.landmark):

                landmarks.append(

                    (
                    idx,
                    lm.x,
                    lm.y
                    )

                )



            self.drawer.draw_landmarks(

                frame,

                hand,

                mp.solutions.hands.HAND_CONNECTIONS

            )



        return frame,landmarks