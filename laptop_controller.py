import pyautogui
import subprocess
import time
import os
from datetime import datetime



class LaptopController:


    def __init__(self):

        self.last_action = None
        self.cooldown = 2
        self.last_time = 0



    def can_execute(self, action):

        current_time = time.time()


        if (
            action == self.last_action
            and current_time - self.last_time < self.cooldown
        ):
            return False


        self.last_action = action
        self.last_time = current_time

        return True



    # -------------------------
    # Volume Controls
    # -------------------------

    def volume_up(self):

        subprocess.run(
            [
                "osascript",
                "-e",
                "set volume output volume ((output volume of (get volume settings)) + 10)"
            ]
        )



    def volume_down(self):

        subprocess.run(
            [
                "osascript",
                "-e",
                "set volume output volume ((output volume of (get volume settings)) - 10)"
            ]
        )



    def mute(self):

        subprocess.run(
            [
                "osascript",
                "-e",
                "set volume with output muted"
            ]
        )



    # -------------------------
    # Screenshot
    # -------------------------

    def screenshot(self):

        folder = "screenshots"

        os.makedirs(
            folder,
            exist_ok=True
        )


        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )


        filename = os.path.join(
            folder,
            f"screenshot_{timestamp}.png"
        )


        image = pyautogui.screenshot()


        image.save(
            filename
        )


        print(
            "Screenshot saved:",
            filename
        )



    # -------------------------
    # Gesture Mapping
    # -------------------------

    def execute(self, gesture):

        actions = {

            # Volume
            "thumbs_up":
                self.volume_up,


            "thumbs_down":
                self.volume_down,


            "open_palm":
                self.mute,


            # Screenshot
            "pinch":
                self.screenshot

        }


        if gesture in actions:


            if self.can_execute(gesture):


                print(
                    "Executing:",
                    gesture
                )


                actions[gesture]()