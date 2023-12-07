import numpy as np
# import matplotlib.pyplot as plt
import numpy as np
# import matplotlib.pyplot as plt
from environment.experimental_blocks import BlackJack,DataLogger
from environment.interface import Interface
# from interface_utils import render_textrect
import pygame
import time



def main():
    debug_mode = True

    # Set up experiment
    practice_timepressure = 10
    low_timepressure = 5
    med_timepressure = 4
    high_timepressure = 3
    Timepressures = [low_timepressure, med_timepressure, high_timepressure]
    np.random.shuffle(Timepressures)
    time_pressure = practice_timepressure
    igame = -1

    BJ = BlackJack()
    player_hand, dealer_hand = BJ.get_hand()

    # Set up utils
    data = DataLogger()
    n_practice = 10
    ready_delay = 5
    ready_tstart = time.time()
    hand_tstart = time.time()
    interface = Interface()
    interface.practice_timepressure = practice_timepressure
    interface.low_timepressure = low_timepressure
    interface.med_timepressure = med_timepressure
    interface.high_timepressure = high_timepressure

    back_rect = None
    next_rect = None
    close_rect = None

    interface.draw_notification(notification_time=5)


if __name__ == "__main__":
    main()
