"""
algorithm/service.py

Project: Pathfinder
Created: 13.10.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from observable import Observable
from typing import Callable
from random import choice

from config import Config

from .points import BasePoint, StartPoint, EndPoint


##################################################
#                     Code                       #
##################################################

class _PointService:
    """
    Service to manage a group of points
    """
    points: list[BasePoint]
    start_points: list[StartPoint]
    end_points: list[EndPoint]

    update: Observable

    def __init__(self) -> None:
        """
        Initialize Service
        """
        self.points = []
        self.start_points = []
        self.end_points = []

        self.update = Observable()

    # Basic point add functions

    def add_random_points(self, num: int | None = Config.number) -> None:
        """
        Add a certain amount of random points

        :param num: Number of points to add
        """
        for index in range(num):
            self.points.append(BasePoint())

        self.update.trigger("add_ran")
        self.update.trigger("*")

    def add_start_points(self, num: int | None = 1) -> None:
        """
        Add a certain amount of starting points

        :param num: Number of starting points to add
        """
        for index in range(num):
            self.start_points.append(StartPoint())

        self.update.trigger("add_start")
        self.update.trigger("*")

    def add_end_points(self, num: int | None = 1) -> None:
        """
        Add a certain amount of end points

        :param num: Number of end points to add
        """
        for index in range(num):
            self.end_points.append(EndPoint())

        self.update.trigger("add_end")
        self.update.trigger("*")

    # Algorithm

    def path_algorithm(
            self,
            start_index: int,
            end_index: int,
            criteria_callback: Callable[[list[tuple[BasePoint, float]]], BasePoint]
    ) -> tuple[list[BasePoint], list[BasePoint]]:
        """
        Create a random path through the field

        :param start_index:
        :param end_index:
        :param criteria_callback:
        :return:
        """

        start_point = self.start_points[start_index]
        goal_id = self.end_points[end_index].id

        path: list[BasePoint] = [start_point]
        no_points: list[int] = []

        point_found: bool = False
        point_in_range: list[tuple[BasePoint, float]] = []

        while not point_found:
            point = path[-1] if path else start_point
            point_in_range = point.get_points_in_range([p.id for p in path] + no_points)
            if point_in_range:
                for p in point_in_range:
                    if p[0].id == goal_id:
                        path.append(p[0])
                        break
                else:
                    path.append(criteria_callback(point_in_range))
            else:
                no_points.append(path[-1].id)
                path = path[:-1]
                continue

            if path[-1].id == goal_id:
                point_found = True

            yield path[-2], point_in_range

        yield path[-1], point_in_range

    def __random_choice_criteria(self, points: list[tuple[BasePoint, float]]) -> BasePoint: # noqa
        """
        Choose a random point out of the list

        :param points: List with points and distances
        :return: A random choosen point
        """
        return choice(points)[0]

    def random_choice_alogrithm(
            self,
            start_index: int | None = 0,
            end_index: int | None = 0
    ) -> tuple[list[BasePoint], list[BasePoint]]:
        """
        Create a random path through the field

        :param start_index:
        :param end_index:
        :return:
        """
        return self.path_algorithm(start_index, end_index, self.__random_choice_criteria)

    def __nearest_criteria(self, points: list[tuple[BasePoint, float]]) -> BasePoint: # noqa
        """
        Choose the nearest point

        :param points: List with points and distances
        :return: The nearest point
        """
        min_point: BasePoint = points[0][0]
        min_dis: float = points[0][1]

        for point in points:
            if point[1] < min_dis:
                min_dis = point[1]
                min_point = point[0]

        return min_point

    def nearest_algorithm(
            self,
            start_index: int | None = 0,
            end_index: int | None = 0
    ) -> tuple[list[BasePoint], list[BasePoint]]:
        """
        Always choose the nearest point

        :param start_index:
        :param end_index:
        :return:
        """
        return self.path_algorithm(start_index, end_index, self.__nearest_criteria)

    def __highest_criteria(self, points: list[tuple[BasePoint, float]]) -> BasePoint:  # noqa
        """
        Choose the nearest point

        :param points: List with points and distances
        :return: The nearest point
        """
        min_point: BasePoint = points[0][0]
        min_dis: float = points[0][1]

        for point in points:
            if point[1] > min_dis:
                min_dis = point[1]
                min_point = point[0]

        return min_point

    def highest_algorithm(
            self,
            start_index: int | None = 0,
            end_index: int | None = 0
    ) -> tuple[list[BasePoint], list[BasePoint]]:
        return self.path_algorithm(start_index, end_index, self.__highest_criteria)

    # Path cutters

    def cut_path(self, path: list[BasePoint]) -> list[BasePoint]:
        for index, point in enumerate(path):
            if point in path[index+1:]:
                shortcut_index = path[index+1:].index(point) + 2 + index
                return self.cut_path(path[:index] + path[shortcut_index:])
        return path

    def cut_path_2(self, path: list[BasePoint]) -> list[BasePoint]:
        for index, point in enumerate(path):
            for point_in_radius in point.get_points_in_range():
                if point_in_radius[0] in path[index+1:] and point_in_radius[0] != path[index+1]:
                    shortcut_index = path[index+1:].index(point_in_radius[0]) + 1 + index
                    return self.cut_path_2(path[:index+1] + path[shortcut_index:])
        return path


PointService = _PointService()
