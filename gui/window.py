"""
gui/window.py

Project: Pathfinder
Created: 13.10.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################
import time

from customtkinter import CTk, CTkCanvas
from time import sleep

from algorithm.service import PointService, BasePoint
from typing import Callable
from config import Config


##################################################
#                     Code                       #
##################################################

class Window(CTk):
    """
    Window to represent the pathfinder-algorithm
    """

    canvas: CTkCanvas

    scale: bool

    tag_count: int

    def __init__(
            self,
            scale: bool | None = False,
            *args: any,
            **kwargs: any
    ) -> None:
        """
        Initialize pathfinder window

        :param args: Positonal arguments passed to CTk
        :param kwargs: Keyword arguments passed to CTk
        """
        self.scale = scale

        super().__init__(*args, **kwargs)
        self.state("zoomed")
        self.title("Pathfinder - Algorithm - GUI")

        self.canvas = CTkCanvas(self)
        self.canvas.configure(background="#000000", bd=0, highlightthickness=0)
        self.update()

        self.tag_count = 0

        self.grid_widgets()
        self.represent_points()

    def draw_points(
            self,
            point_list: list[BasePoint],
            radius_color: str | None = Config.radius_color,
            point_radius: int | None = Config.point_radius,
            point_color: str | None = Config.point_color
    ) -> None:
        """

        :param point_list:
        :param radius_color:
        :param point_radius:
        :param point_color:
        :return:
        """
        for point in point_list:
            self.canvas.create_oval(point.cord_x - point.radius, point.cord_y - point.radius,
                                    point.cord_x + point.radius, point.cord_y + point.radius,
                                    outline=radius_color, tags="points")

        for point in point_list:
            self.canvas.create_aa_circle(int(point.cord_x), int(point.cord_y),
                                         radius=point_radius,
                                         fill=point_color, tags="points")

    def represent_points(self) -> None:
        self.canvas.delete("all")

        self.draw_points(PointService.start_points,
                         point_color=Config.start_color,
                         point_radius=Config.start_radius)

        self.draw_points(PointService.end_points,
                         point_color=Config.end_color,
                         point_radius=Config.end_radius)

    def run_alogrithm(
            self,
            alg_func: Callable,
            cutting: bool | None = True,
            tag: str | None = None,
            path_color: str | None = Config.path_color,
    ) -> None:
        tag = tag
        if not tag:
            tag = f"TAG{self.tag_count}"
            self.tag_count += 1
        path: list[BasePoint] = []

        for point, found_points in alg_func():
            self.draw_points([point[0] for point in found_points])
            if path:
                self.canvas.create_line(point.cord_x, point.cord_y,
                                        path[-1].cord_x, path[-1].cord_y,
                                        fill=path_color, width=3, tag=tag)
                self.canvas.update()
            path.append(point)

        if cutting:
            self.canvas.delete(tag)

            def cut(path_):
                for point_ in PointService.cut_path_2(path_):
                    yield point_, []

            self.run_alogrithm(lambda: cut(path), False)

    def draw_path(self, path: list[BasePoint]) -> None:
        for index, point in enumerate(path[:-1]):
            self.canvas.create_line(point.cord_x, point.cord_y,
                                    path[index+1].cord_x, path[index+1].cord_y,
                                    fill=Config.path_color, width=3)

    def grid_widgets(self) -> None:
        """
        Grid all widgets
        """
        self.canvas.grid(row=0, column=0, sticky="NSEW")
        self.grid_rowconfigure(0, weight=10)
        self.grid_columnconfigure(0, weight=10)
