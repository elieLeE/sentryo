# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Specie(object):
    """
    Class representing a specie.
    """
    def __init__(self, _id, name, classification="", designation="", averageHeight="", skinColors="", hairColors="",
                 eyeColors="", averageLifeSpan="", homeWorld="", language="", peoplesBelongSpecieList=None,
                 filmsList=None):
        self._id = _id
        self._name = name
        self._classification = classification
        self._designation = designation
        self._averageHeight = averageHeight
        self._skinColors = skinColors
        self._hairColors = hairColors
        self._eyeColors = eyeColors
        self._averageLifeSpan = averageLifeSpan
        self._homeWorld = homeWorld
        self._language = language
        self._peopleBelongSpecieList = peoplesBelongSpecieList if peoplesBelongSpecieList is not None else []
        self._filmsList = filmsList if filmsList is not None else []

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def __str__(self):
        info = "Name : {}\nClassification : {}, Designation : {}\nAverage height : {}Average life span : {}\n" \
               "Skin colors : {}, Hair colors : {}, Eye colors : {}\nHomeworld : {}, language : {}\n" \
               "People belong this specie : {}\nSpecie appeared in films {}\n".\
            format(self._name, self._classification, self._designation, self._averageHeight, self._averageLifeSpan,
                   self._skinColors, self._hairColors, self._eyeColors, self._homeWorld, self._language,
                   self._peopleBelongSpecieList, self._filmsList)

        return info

    def getStr(self):
        return self.__str__()

