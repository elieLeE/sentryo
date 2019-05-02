# !/usr/bin/env python
# -*- coding: utf-8 -*-


class People(object):
    """
    Class representing a people.
    """
    def __init__(self, _id, name, height, mass, hairColor, skinColor, eyeColor, birthYear, gender, homeWorld,
                 dateCreated, dateEdited, vehicles, starShips, filmsList, speciesList):
        self._id = _id
        self._name = name
        self._height = height
        self._mass = mass
        self._hairColor = hairColor
        self._skinColor = skinColor
        self._eyeColor = eyeColor
        self._birthYear = birthYear
        self._gender = gender
        self._homeWorld = homeWorld
        self._dateCreated = dateCreated
        self._dateEdited = dateEdited
        self._starShipsList = starShips
        self._vehiclesList = vehicles
        self._filmsList = filmsList
        self._speciesList = speciesList

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def setName(self, newName):
        self._name = newName

    def getHeight(self):
        return self._height

    def setHeight(self, newHeight):
        self._height = newHeight

    def getMass(self):
        return self._mass

    def setMass(self, newMass):
        self._mass = newMass

    def getHairColor(self):
        return self._hairColor

    def setHairColor(self, newHairColor):
        self._hairColor = newHairColor

    def getSkinColor(self):
        return self._skinColor

    def setSkinColor(self, newSkinColor):
        self._skinColor = newSkinColor

    def getEyeColor(self):
        return self._eyeColor

    def setEyeColor(self, newEyeColor):
        self._eyeColor = newEyeColor

    def getBirthYear(self):
        return self._birthYear

    def setBirthDay(self, newBirthDay):
        self._birthYear = newBirthDay

    def getGender(self):
        return self._gender

    def setGender(self, newGender):
        self._gender = newGender

    def getHomeWorld(self):
        return self._homeWorld

    def setHomeWorld(self, newHomeWorld):
        self._homeWorld = newHomeWorld

    def getDateCreated(self):
        return self._dateCreated

    def getDateEdited(self):
        return self._dateEdited

    def getStarShips(self):
        return self._starShipsList

    def addStarShip(self, starShipName):
        self._starShipsList.append(starShipName)

    def removeStarShip(self, starShipName):
        self._starShipsList.remove(starShipName)

    def getVehicles(self):
        return self._vehiclesList

    def addVehicle(self, vehicleName):
        self._vehiclesList.append(vehicleName)

    def removeVehicle(self, vehicleName):
        self._vehiclesList.remove(vehicleName)

    def getFilms(self):
        return self._filmsList

    def getSpecies(self):
        return self._speciesList

    def __str__(self):
        info = "Name : {}\nBirth year : {}, HomeWorld: {}\nGender : {}\nHeight : {}, Mass : {}\n" \
               "Hair Color : {}, Skin color : {}, Eye color : {}\nStar ships : {}\nVehicles : {}\n" \
               "Films in which this people appears : {}\n" \
               "Specie of this people : {}".\
            format(self._name, self._birthYear, self._homeWorld, self._gender, self._height, self._mass,
                   self._hairColor, self._skinColor, self._eyeColor, self._starShipsList, self._vehiclesList,
                   self._filmsList, self._speciesList)

        return info

    def getStr(self):
        return self.__str__()
