from laptop_controller import LaptopController
import time


controller = LaptopController()


controller.play_pause()

time.sleep(5)

controller.next_track()