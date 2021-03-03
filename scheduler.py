"""Assignment 1 - Scheduling algorithms (Task 4)

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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """A random scheduler, randomly decide what parcels go onto which trucks.

    === Private Attributes ===
    _parcels:
      A list of parcels <Parcel> to be scheduled to the trucks.

    === Representation Invariants ===
    - No parcels have the depot as their destination.
    - Each truck has its own unique id.
    """
    _parcels: List[Parcel]

    def __init__(self) -> None:
        """Instantiate the class."""
        self._parcels = []

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto a random chosen truck.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        self._parcels = parcels[:]
        unscheduled = []
        shuffle(self._parcels)
        for parcel in self._parcels:
            va_trucks = []  # a list of all trucks that have the capacity
            for truck in trucks:
                if truck.unused_space() >= parcel.volume:
                    va_trucks.append(truck)
            if len(va_trucks) == 0:
                unscheduled.append(parcel)
            else:
                choice(va_trucks).pack(parcel)

        return unscheduled


class GreedyScheduler(Scheduler):
    """A systematic scheduler, strategically decide what parcels go onto
    which trucks.

    === Private Attributes ===
    _priority:
      Either 'volume' or 'destination'.
    _par:
      Either 'non-decreasing' or 'non-increasing'.
    _trk:
      Either 'non-decreasing' or 'non-increasing'.

    === Representation Invariants ===
    - No parcels have the depot as their destination.
    - Each truck has its own unique id.
    """
    _priority: str
    _par: str
    _trk: str

    def __init__(self, priority: str, par_order: str, trk_order: str) -> None:
        """Instantiate the class. <priority> is the parcel_priority from config:
        either 'volume' or 'destination'. <par_order> is the parcel_order from
        config: either 'non-decreasing' or 'non-increasing'. <trk_order> is the
        truck_order from config: either 'non-decreasing' or 'non-increasing'.
        """
        self._priority = priority
        self._par = par_order
        self._trk = trk_order

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto a truck from <trucks> processes
        parcels one at a time, picking a truck for each, but it tries to pick
        the “best” truck it can for each parcel.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        unscheduled = []
        pq = _choose(self._priority, self._par)
        _add_queue(parcels, pq)
        while not pq.is_empty():
            parcel = pq.remove()
            va_truck = []  # a list of all trucks that have the capacity
            bt_truck = []  # a list of trucks that have capacity and have
            # the parcel’s destination at the end of their route
            _mutates_lists(parcel, trucks, va_truck, bt_truck)  # Call helper

            if len(va_truck) == 0:
                unscheduled.append(parcel)
            elif len(bt_truck) == 0:
                use_truck = va_truck
                temp = _find_best_truck(use_truck, self._trk)
                temp.pack(parcel)
            else:
                use_truck = bt_truck
                temp = _find_best_truck(use_truck, self._trk)
                temp.pack(parcel)
        return unscheduled


def _find_best_truck(trucks: List[Truck], order: str) -> Truck:
    """Return the 'best' Truck in <trucks> that satisfies <order>."""
    temp = trucks[0]
    if order == 'non-decreasing':
        for truck in trucks:
            if truck.unused_space() < temp.unused_space():
                temp = truck
    else:
        for truck in trucks:
            if truck.unused_space() > temp.unused_space():
                temp = truck
    return temp


def _mutates_lists(p: Parcel, trucks: List[Truck], va: List, bt: List) -> None:
    """Mutates <va> and <bt> with correspondence with <p> and <trucks>."""
    for truck in trucks:
        if truck.unused_space() >= p.volume \
                and truck.routes[-1] == p.destiny:
            va.append(truck)
            bt.append(truck)
        elif truck.unused_space() >= p.volume:
            va.append(truck)


def _add_queue(parcels: List[Parcel], priority_q: PriorityQueue) -> None:
    """add <parcels> to <priority>. Implemented only for GreedyScheduler
    schedule method."""
    for parcel in parcels:
        priority_q.add(parcel)


def _choose(priority: str, order: str) -> PriorityQueue:
    """Return a PriorityQueue in regards with the parcel priority and
    parcel order.

    precondition: <priority> is either 'volume' or 'destination'
                  <order> is either 'non-decreasing' or 'non-increasing'
    """
    if priority == 'volume' and order == 'non-decreasing':
        return PriorityQueue(_incr_volume)
    if priority == 'volume' and order == 'non-increasing':
        return PriorityQueue(_decr_volume)
    if priority == 'destination' and order == 'non-decreasing':
        return PriorityQueue(_incr_dest)

    return PriorityQueue(_decr_dest)


def _incr_volume(p1: Parcel, p2: Parcel) -> bool:
    """Return True if <p1> has lesser volume than <p2>.
    """
    return p1.volume < p2.volume


def _decr_volume(p1: Parcel, p2: Parcel) -> bool:
    """Return True if <p1>.volume is higher than <p2>.volume."""
    return p1.volume > p2.volume


def _incr_dest(p1: Parcel, p2: Parcel) -> bool:
    """Return True if <p1>'s destination is alphabetically smaller than <p2>'s
    destination."""
    return p1.destiny < p2.destiny


def _decr_dest(p1: Parcel, p2: Parcel) -> bool:
    """Return True if <p1>'s destination is alphabetically larger than <p2>'s
    destination."""
    return p1.destiny > p2.destiny


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
