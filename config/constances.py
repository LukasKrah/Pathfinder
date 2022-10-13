"""
config/constances.py

Project: Pathfinder
Created: 13.10.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from dataclasses import dataclass


##################################################
#                     Code                       #
##################################################

@dataclass(frozen=True)
class Config:
    # Field configuration
    width: float = 1920.0
    height: float = 1080.0
    points: float = 100.0
    margin: float = 10.0

    # Point configuartion
    radius: tuple[float] = (150,)
    number: int = 500

    # GUI
    point_radius: int = 3
    start_radius: int = 10
    end_radius: int = 10
    point_color: str = "#FFFFFF"
    start_color: str = "#FFFF00"
    end_color: str = "#00FF00"
    radius_color: str = "#0000FF"
    path_color: str = "#FF0000"
