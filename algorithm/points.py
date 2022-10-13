"""
algorithm/points.py

Project: Pathfinder
Created: 13.10.2022
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from random import uniform, choice

from config import Config


##################################################
#                     Code                       #
##################################################

class BasePoint:
    """
    Represents a basic point
    """
    all_points: list["BasePoint"] = []

    cord_x: float
    cord_y: float
    radius: float

    id: int

    def __init__(
            self,
            cord_x: float | None = None,
            cord_y: float | None = None,
            radius: float | None = None
    ) -> None:
        """
        Create a basic point with coords and radio radius

        :param cord_x: Coordination on the x-axis
        :param cord_y: Coordination on the y-axis
        :param radius: Radio radius of the point
        """
        self.id = len(self.all_points)
        self.__class__.all_points.append(self)

        self.cord_x = cord_x if cord_x else uniform(Config.margin, Config.width-Config.margin)
        self.cord_y = cord_y if cord_y else uniform(Config.margin, Config.height-Config.margin)

        self.radius = radius if radius else choice(Config.radius)

    def get_points_in_range(self, not_ids: list[int] | None = []) -> list[tuple["BasePoint", float]]:
        """
        Function to get all Points in range with distance

        :return: Points which are in range
        """
        points_in_range: list[tuple["BasePoint", float]] = []

        for point in self.all_points:
            if point.id != self.id and point.id not in not_ids:
                distance_x = abs(self.cord_x - point.cord_x)
                distance_y = abs(self.cord_y - point.cord_y)
                distance = (distance_x**2 + distance_y**2) ** 0.5
                if distance <= self.radius:
                    points_in_range.append((point, distance))

        return points_in_range


class StartPoint(BasePoint):
    """
    The starting point of the algorithm
    """

    def __init__(
            self,
            cord_x: float | None = None,
            cord_y: float | None = None,
            radius: float | None = None
    ) -> None:
        """
        Create a starting point with coords and radio radius

        :param cord_x: Coordination on the x-axis
        :param cord_y: Coordination on the y-axis
        :param radius: Radio radius of the point
        """

        super().__init__(cord_x, cord_y, radius)


class EndPoint(BasePoint):
    """
    The end point to find
    """

    def __init__(
            self,
            cord_x: float | None = None,
            cord_y: float | None = None,
            radius: float | None = None
    ) -> None:
        """
        Create a end point with coords and radio radius

        :param cord_x: Coordination on the x-axis
        :param cord_y: Coordination on the y-axis
        :param radius: Radio radius of the point
        """

        super().__init__(cord_x, cord_y, radius)
