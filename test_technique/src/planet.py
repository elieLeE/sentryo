# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Planet(object):
    """
    Class representing a planet.
    """
    def __init__(self, name, rotationPeriod, orbitalPeriod, diameter, climate, gravity, terrain, surfaceWater,
                 population, filmsList):
        self._name = name
        self._rotationPeriod = rotationPeriod
        self._orbitalPeriod = orbitalPeriod
        self._diameter = diameter
        self._climate = climate
        self._gravity = gravity
        self._terrain = terrain
        self._surfaceWater = surfaceWater
        self._population = population
        self._filmsList = filmsList

    def getName(self):
        return self._name

    def __str__(self):
        info = "Name : {}\nRotation period : {}, Orbital period : {}\nDiameter : {}, Gravity : {}\n" \
               "Climate : {}, Terrain : {}, Surface water : {}\nFilms where the planet appeared: {}\n".\
            format(self._name, self._rotationPeriod, self._orbitalPeriod, self._diameter, self._gravity, self._climate,
                   self._terrain, self._surfaceWater, self._filmsList)

        return info

    def getStr(self):
        return self.__str__()
