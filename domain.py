"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """ A parcel that contain an unique ID, source, destiny, and volume.

    === Public Attributes ===
    id:
      The unique id of this parcel.
    source:
      Where the parcel is from.
    destiny:
      Where the parcel needs to be delivered to.
    volume:
      The volume of this parcel.

    === Representation Invariants ===
    - <_id> can only occur once for parcels of <_parcels>.
    - <_volume> is a positive integer.
    - No parcels have the depot as their destination.
    """
    id: int
    source: str
    destiny: str
    volume: int

    def __init__(self, id_: int, vol: int, sour: str, dest: str) -> None:
        """Instantiates the Parcel class. <id_> is the unique id of this parcel,
        <vol> is the volume, <sour> is where the parcel came from, and <dest> is
        its destination.

        precondition: <vol> > 0
        """
        self.id = id_
        self.volume = vol
        self.source = sour
        self.destiny = dest


class Truck:
    """ A truck that contains information of its capacity and id.

    === Public Attributes ===
    capacity:
      Determines how much this truck can hold.
    routes:
      A list of places the truck needs to go to.
    parcels:
      A list of <Parcel> that were stored in the truck.
    current:
      The current volume of stuff in this truck.
    id:
      The unique id of this truck.

    === Private Attributes ===

    === Representation Invariants ===
    - len(routes) == 1 initially, with only the depot city in it.
    - Each truck has a unique _id, that is, no two
    trucks can have the same _id.
    - <capacity> is a positive integer
    """
    capacity: int
    routes: List[str]
    parcels: List[Parcel]
    current: int
    id: int

    def __init__(self, id_: int, vol: int, depot: str) -> None:
        """Instantiates the class <Truck> with <id_> and <vol>.

        precondition: <vol> > 0
        """
        self.id = id_
        self.capacity = vol
        self.routes = [depot]
        self.current = 0
        self.parcels = []

    def pack(self, p: Parcel) -> bool:
        """Add <p> parcel into the truck. Return True if and only if <p> is
        packed into <Truck>. Return False otherwise.

        >>> t1 = Truck(1, 100, 'Toronto')
        >>> p1 = Parcel(1, 20, 'Toronto', 'Guelph')
        >>> t1.pack(p1)
        True
        >>> t1.routes == ['Toronto', 'Guelph']
        True
        >>> p2 = Parcel(2, 90, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        False
        >>> p3 = Parcel(3, 10, 'Toronto', 'Guelph')
        >>> t1.pack(p3)
        True
        >>> t1.routes == ['Toronto', 'Guelph']
        True
        """
        if self.capacity - self.current >= p.volume:
            self.current += p.volume
            self.parcels.append(p)
            if self.routes[-1] != p.destiny:
                self.routes.append(p.destiny)
            return True
        return False

    def fullness(self) -> float:
        """Return the percentage of fullness for this truck.

        precondition: <self.current> <= <self.capacity>

        >>> t1 = Truck(1, 100, 'Toronto')
        >>> p1 = Parcel(1, 20, 'Toronto', 'Guelph')
        >>> t1.pack(p1)
        True
        >>> t1.fullness()
        20.0
        >>> p2 = Parcel(2, 90, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        False
        >>> t1.fullness()
        20.0
        >>> p3 = Parcel(3, 50, 'Toronto', 'Montreal')
        >>> t1.pack(p3)
        True
        >>> t1.fullness()
        70.0
        """
        return self.current * 100 / self.capacity

    def is_empty(self) -> bool:
        """Return True if <self> is empty, false otherwise.

        >>> t1 = Truck(1, 100, 'Toronto')
        >>> t1.is_empty()
        True
        >>> p1 = Parcel(1, 20, 'Toronto', 'Guelph')
        >>> t1.pack(p1)
        True
        >>> t1.is_empty()
        False
        """
        return self.fullness() == 0

    def unused_space(self) -> int:
        """Return the unused space for this truck.

        >>> t1 = Truck(1, 100, 'Toronto')
        >>> p1 = Parcel(1, 20, 'Toronto', 'Guelph')
        >>> t1.pack(p1)
        True
        >>> t1.unused_space()
        80
        """
        return self.capacity - self.current


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        """

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        num = 0
        for truck in self.trucks:
            if not truck.is_empty():
                num += 1
        return num

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        d = {}
        for truck in self.trucks:
            d[truck.id] = []
            for parcel in truck.parcels:
                d[truck.id].append(parcel.id)
        return d

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        space = 0
        for truck in self.trucks:
            if not truck.is_empty():
                space += truck.unused_space()
        return space

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        num = 0.0
        for truck in self.trucks:
            if not truck.is_empty():
                num += truck.fullness()
        return num

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        return self._total_fullness() / self.num_nonempty_trucks()

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        distance = 0
        for truck in self.trucks:
            for i in range(1, len(truck.routes)):
                distance += dmap.distance(truck.routes[i - 1], truck.routes[i])
            distance += dmap.distance(truck.routes[-1], truck.routes[0])
        return distance

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        return self.total_distance_travelled(dmap) / self.num_nonempty_trucks()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
