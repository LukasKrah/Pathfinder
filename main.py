"""
/main.py

Project: Pathfinder
Created: 13.10.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from algorithm import PointService
from gui import Window


##################################################
#                     Code                       #
##################################################

if __name__ == "__main__":
    PointService.add_start_points()
    PointService.add_end_points()
    PointService.add_random_points()

    win = Window(scale=False)

    win.run_alogrithm(PointService.random_choice_alogrithm)
    win.run_alogrithm(PointService.nearest_algorithm)
    win.run_alogrithm(PointService.highest_algorithm)

    win.mainloop()
