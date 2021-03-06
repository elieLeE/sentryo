# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Vehicle(object):
    """
    Class representing a vehicle.
    """
    def __init__(self, _id, name, model="", manufacturer="", cost="", length="", maxSpeed="", crew="", passengers="", capacity="",
                 consumables="", vehicleClass=""):
        self._name = name
        self._id = _id
        self._model = model
        self._manufacturer = manufacturer
        self._cost = cost
        self._length = length
        self._maxSpeed = maxSpeed
        self._crew = crew
        self._passengers = passengers
        self._capacity = capacity
        self._consumables = consumables
        self._starShipsClass = vehicleClass

    def getName(self):
        return self._name

    def getId(self):
        return self._id

    def __str__(self):
        info = "Name : {}\nModel : {}, Manufacturer : {}, Cost : {}\nLength : {}, Max speed : {}\nCrew : {}, " \
               "Passengers : {}, Capacity : {}\nConsumables : {}\nStar ship class : {}\n". \
            format(self._name, self._model, self._manufacturer, self._cost, self._length, self._maxSpeed, self._crew,
                   self._passengers, self._capacity, self._consumables, self._starShipsClass)

        return info

    def getStr(self):
        return self.__str__()
