import cv2
import time
from collections import deque, Counter

from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from laptop_controller import LaptopController



# -----------------------------
# Initialize components
# -----------------------------

tracker = HandTracker()

detector = GestureDetector()

controller = LaptopController()



# -----------------------------
# Camera
# -----------------------------

cap = cv2.VideoCapture(0)



# -----------------------------
# Gesture smoothing
# -----------------------------

gesture_history = deque(
    maxlen=8
)


previous_gesture = None

last_action_time = 0


ACTION_DELAY = 2   # seconds



# -----------------------------
# Main loop
# -----------------------------

while True:


    ret, frame = cap.read()


    if not ret:
        break



    # Mirror camera
    frame = cv2.flip(
        frame,
        1
    )



    # Detect hand
    frame, landmarks = tracker.get_landmarks(
        frame
    )



    # Predict gesture
    gesture = detector.detect(
        landmarks
    )



    # Ignore invalid predictions
    if gesture not in [
        "None",
        "Unknown"
    ]:

        gesture_history.append(
            gesture
        )



    # Majority voting
    confirmed_gesture = "None"


    if len(gesture_history) >= 5:

        confirmed_gesture = Counter(
            gesture_history
        ).most_common(1)[0][0]



    current_time = time.time()



    # -----------------------------
    # Execute action
    # -----------------------------

    if confirmed_gesture != "None":


        if (
            confirmed_gesture != previous_gesture
            and current_time - last_action_time > ACTION_DELAY
        ):


            print(
                "Executing gesture:",
                confirmed_gesture
            )


            controller.execute(
                confirmed_gesture
            )


            previous_gesture = confirmed_gesture

            last_action_time = current_time




    # -----------------------------
    # Display
    # -----------------------------

    cv2.putText(

        frame,

        f"Gesture: {confirmed_gesture}",

        (20,40),

        cv2.FONT_HERSHEY_SIMPLEX,

        1,

        (0,255,0),

        2

    )



    cv2.imshow(
        "Gesture Control",
        frame
    )



    # Quit
    if cv2.waitKey(1) == ord("q"):

        break



# Cleanup

cap.release()

cv2.destroyAllWindows()