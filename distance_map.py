"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import List, Union


class DistanceMap:
    """A class that lets client code store and look up the distance
    between any two cities.

    === Private Attributes ===
    _distances:
      A list that contains lists of distance between any two cities.
    """
    _distances: List[List[Union[str, int]]]

    def __init__(self) -> None:
        """Initializes the class."""
        self._distances = []

    def distance(self, city1: str, city2: str) -> int:
        """Returns an integer which is the distance from <city1> to <city2>.

        if there is no distance from <city1> to <city2> stored in DistanceMap,
        then return -1

        >>> dm = DistanceMap()
        >>> dm.distance('Toronto', 'Mississauga')
        -1
        >>> dm.add_distance('Toronto', 'Mississauga', 10, 20)
        >>> dm.distance('Toronto', 'Mississauga')
        10
        >>> dm.distance('Mississauga', 'Toronto')
        20
        """
        for dist in self._distances:
            if dist[0] == city1 and dist[1] == city2:
                return dist[2]
            if dist[1] == city1 and dist[0] == city2:
                return dist[3]
        return -1

    def add_distance(self, c1: str, c2: str, d1: int, d2: int = 0) -> None:
        """Add distance <d1> from <c1> to <c2> and distance <d2> from <c2> to
        <c1> to DistanceMap.

        >>> dm = DistanceMap()
        >>> dm.add_distance('Toronto', 'Guelph', 10)
        >>> dm.distance("Toronto", "Guelph")
        10
        >>> dm.distance('Guelph', 'Toronto')
        10
        """
        if d2 == 0:
            d2 = d1
            self._distances.append([c1, c2, d1, d2])
        else:
            self._distances.append([c1, c2, d1, d2])


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest

    doctest.testmod()
