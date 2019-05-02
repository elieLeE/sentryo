# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import datetime
from request_builder import TablePeopleRequestBuilder, TableVehiclesRequestBuilder, TableStarShipsRequestBuilder, \
    TablePeopleStarShipsRequestBuilder, TableFilmsRequestBuilder, TableSpeciesRequestBuilder, \
    TablePlanetsRequestBuilder, TablePeopleVehiclesRequestBuilder, TableFilmsPeopleRequestBuilder, \
    TablePeopleSpeciesRequestBuilder
from defines import TablePeople
from people import People
from starships import StartShip
from vehicle import Vehicle
from specie import Specie
from films import Film
from planet import Planet


class DataBaseManager(object):
    """
    Class letting to send request to data base.
    It uses the inherited class of RequestBuilder in order to retrieve the request, send it to data base
    and retrieve results.
    """
    def __init__(self):
        super(DataBaseManager, self).__init__()
        self._connectionObj = None
        self._cursor = None

    def _encodeRes(self, rowRes):
        """Encode to utf-8 all results obtained from data base.

        :param rowRes: data in a tuple.
        :return: a tuple with the data encoded.
        """
        for i in range(len(rowRes)):
            res = rowRes[i]
            if res is not None:
                rowRes[i] = res.encode("utf-8")
        return rowRes

    def openConnection(self, dataBaseFile):
        """Open a connection between the application and the data base.

        :param dataBaseFile: path to the data base file- str.
        :return: None
        """
        self._connectionObj = sqlite3.connect(dataBaseFile)

    def closeConnection(self):
        """Close the connection between the application and the data base.

        :return:
        """
        self._connectionObj.close()

    def _sendRequest(self, stringRequest):
        """Send a request to the data base.

        :param stringRequest: str.
        :return: sqlite3.Cursor object.
        """
        self._cursor = self._connectionObj.cursor()
        return self._cursor.execute(stringRequest)

    def getStarShipsInfo(self, starShipsNameList=None, completeInfo=True):
        """Method letting to retrieve data of star ship table.

        :param starShipsNameList: the row the user wants to retrieve. If None, all row are retrieved.
        :param completeInfo: boolean indicating if we want to retrieve all columns and just minimal.
        :return: list of StartShip instance.
        """
        req = TableStarShipsRequestBuilder().getStarShipsInfoRequest(starShipsNameList, completeInfo)
        starShipsList = []
        for row in self._sendRequest(req):
            starShipsList.append(StartShip(*row))

        return starShipsList

    def getVehiclesInfo(self, vehiclesNameList=None, completeInfo=True):
        """Method letting to retrieve data of vehicle table.

        :param vehiclesNameList: the row the user wants to retrieve. If None, all row are retrieved.
        :param completeInfo: boolean indicating if we want to retrieve all columns and just minimal.
        :return: list of Vehicle instance.
        """
        req = TableVehiclesRequestBuilder().getVehiclesInfoRequest(vehiclesNameList, completeInfo)

        vehiclesList = []
        for row in self._sendRequest(req):
            vehiclesList.append(Vehicle(*row))

        return vehiclesList

    def addStarShipToPeople(self, idPeople, idStarShip):
        """Method letting to add a new row in starship-people table (the user has added a star ship to an user).

        :param idPeople: id of the people - str.
        :param idStarShip: id of the star ship - str.
        :return: None.
        """
        request = TablePeopleStarShipsRequestBuilder().getInsertRowRequest(idPeople, idStarShip)
        self._sendRequest(request)
        self._connectionObj.commit()

    def addVehicleToPeople(self, idPeople, idVehicle):
        """Method letting to add a new row in vehicle-people table (the user has added a vehicle to an user).

        :param idPeople: id of the people - str.
        :param idVehicle: id of the vehicle - str.
        :return: None.
        """
        request = TablePeopleVehiclesRequestBuilder().getInsertRowRequest(idPeople, idVehicle)
        self._sendRequest(request)
        self._connectionObj.commit()

    def removeStarShipFromPeople(self, idPeople, idStarShip):
        """Method letting to remove a row from starship-people table (the user has removed a star ship to an user).

        :param idPeople: id of the people - str.
        :param idStarShip: id of the vehicle - str.
        :return: None.
        """
        request = TablePeopleStarShipsRequestBuilder().getDeleteRowRequest(idPeople, idStarShip)
        self._sendRequest(request)
        self._connectionObj.commit()

    def removeVehicleFromPeople(self, idPeople, idVehicle):
        """Method letting to remove a row from vehicle-people table (the user has removed a star ship to an user).

        :param idPeople: id of the people - str.
        :param idVehicle: id of the vehicle - str.
        :return: None.
        """
        request = TablePeopleVehiclesRequestBuilder().getDeleteRowRequest(idPeople, idVehicle)

        self._sendRequest(request)
        self._connectionObj.commit()

    def addFilmsToPeople(self, idPeople, idFilm):
        """Method letting to add a new row in films-people table (the user has added a film to an user).

        :param idPeople: id of the people - str.
        :param idFilm: id of the vehicle - str.
        :return: None.
        """
        request = TableFilmsPeopleRequestBuilder().getInsertRowRequest(idPeople, idFilm)
        self._sendRequest(request)
        self._connectionObj.commit()

    def addSpecieToPeople(self, idPeople, idSpecie):
        """Method letting to add a new row in species-people table (the user has added a spacie to an user).

        :param idPeople: id of the people - str.
        :param idSpecie: id of the vehicle - str.
        :return: None.
        """
        request = TablePeopleSpeciesRequestBuilder().getInsertRowRequest(idPeople, idSpecie)
        self._sendRequest(request)
        self._connectionObj.commit()

    def _unifyRow(self, rowList):
        """The request has not enough evolved in order to group data corresponding to the same elements
        with a micro difference.
        For example, if I want to retrieve a people with all theses vehicles associated, I would like to have a row
        and, in it, a list with all vehicles names. But, apparently, this does not well. So, we will retrieve several
        items for each differences. In this method, we group all this row.

        :param rowList: list of row (tuple).
        :return: dict of row (tuple) with as id the first item of the row.
        """
        dictRow = {}
        for row in rowList:
            _id = row[0]
            listRow = dictRow.get(_id, [])
            listRow.append(row)
            if len(listRow) == 1:
                dictRow[_id] = listRow

        return dictRow

    def _cleanRow(self, rowList, listItemIndex):
        """Clean row retrieved from the data base.
        This method do two things :
            - encode in utf-8 all data retrieved data base.
            - merged some row corresponding to the almost same info in a one row.

        :param rowList:
        :param listItemIndex:
        :return: a unique list correspond to all rows merged.
        """
        listItemsValues = [[] for _ in xrange(len(listItemIndex))]
        dictIdxListValues = {}
        for i, idx in enumerate(listItemIndex):
            dictIdxListValues[idx] = i

        for row in rowList:
            for idx in listItemIndex:
                val = row[idx].encode("utf-8") if row[idx] is not None else ""
                listVal = listItemsValues[dictIdxListValues[idx]]
                if val not in listVal:
                    listVal.append(val)
        r = self._encodeRes(list(rowList[0]))
        for idx in listItemIndex:
            r[idx] = listItemsValues[dictIdxListValues[idx]]

        return r

    def getPeopleInfo(self, personNameList=None):
        """Method letting to retrieve data of people table.

        :param personNameList: the row the user wants to retrieve. If None, all row are retrieved.
        :return: list of People instance.
        """
        peopleObjects = []

        dictRow = self._unifyRow(self._sendRequest(TablePeopleRequestBuilder().getPeoplesInfoRequest(personNameList)))
        for rowList in dictRow.itervalues():
            peopleObjects.append(People(*self._cleanRow(rowList, [12, 13, 14, 15])))

        return peopleObjects

    def getNewIdPeople(self):
        """Retrieve a unique id for a new people.
        Count the row and return the number +1.

        :return: the new id - str.
        """
        self._sendRequest(TablePeopleRequestBuilder().getCountRowTableRequest())
        self._connectionObj.commit()
        peopleTableCount = self._cursor.fetchone()[0]
        return str(peopleTableCount + 1)

    def addNewPeople(self, peopleObject):
        """Add a new people to the people table.

        :param peopleObject: People instance - contain the data of the new people,
        so the data of the new row we will create.
        :return: None?.
        """
        request = TablePeopleRequestBuilder().getInsertRowRequest(peopleObject)
        self._sendRequest(request)
        self._connectionObj.commit()

    def updatePeopleInfo(self, peopleId, newData):
        """Update rows corresponding to data people (row in people table and row in starships-people, vehicles-people,
        films-people and species-people).

        :param peopleId: the id of the people to update - str.
        :param newData: the new data - dict with the new data, and only the new data.
        :return: None.
        """
        if newData:
            # first, we update the row of people table.
            newData[TablePeople.COLUMN_DATA_EDITED] = datetime.datetime.utcnow()
            newPeopleData = {k: v for k, v in newData.iteritems()
                             if (k != TablePeople.COLUMN_STAR_SHIPS) and (k != TablePeople.COLUMN_VEHICLES)}

            if newPeopleData:
                req = TablePeopleRequestBuilder().getUpdatePeopleInfoRequest(peopleId, newPeopleData)
                self._sendRequest(req)
                self._connectionObj.commit()

            # then, we update the dat in starships-people, vehicles-people, films-people and species-people.
            # As to say, we add or remove some rows in these tables.
            starShipsData = newData.get(TablePeople.COLUMN_STAR_SHIPS, {})
            for starShipIdToRemove in starShipsData.get(0, []):
                self.removeStarShipFromPeople(peopleId, starShipIdToRemove)

            for starShipIdToAdd in starShipsData.get(1, []):
                self.addStarShipToPeople(peopleId, starShipIdToAdd)

            vehiclesData = newData.get(TablePeople.COLUMN_VEHICLES, {})
            for vehicleIdToRemove in vehiclesData.get(0, []):
                self.removeVehicleFromPeople(peopleId, vehicleIdToRemove)

            for vehicleIdToAdd in vehiclesData.get(1, []):
                self.addVehicleToPeople(peopleId, vehicleIdToAdd)

    def deletePeople(self, peopleId):
        """Delete a row from people table.

        :param peopleId: the id of the people to remove - str.
        :return: None.
        """
        self._sendRequest(TablePeopleRequestBuilder().getDeleteRequest(peopleId))
        self._connectionObj.commit()

    def getFilmsInfo(self, filmsNameList, completeInfo=True):
        """Method letting to retrieve data of films table.

        :param filmsNameList: the row the user wants to retrieve. If None, all row are retrieved.
        :param completeInfo: boolean indicating if we want to retrieve all columns and just minimal.
        :return: list of Film instance.
        """
        filmsList = []

        listRow = self._sendRequest(TableFilmsRequestBuilder().getFilmsInfoRequest(filmsNameList, completeInfo))
        dictRow = self._unifyRow(listRow)
        for rowList in dictRow.itervalues():
            if completeInfo:
                r = self._cleanRow(rowList, [7, 8, 9, 10, 11])
            else:
                r = self._cleanRow(rowList, [])
            filmsList.append(Film(*r))

        return filmsList

    def getPlanetsInfo(self, planetsNamesList):
        """Method letting to retrieve data of planets table.

        :param planetsNamesList: the row the user wants to retrieve. If None, all row are retrieved.
        :return: list of Planet instance.
        """
        planetsList = []

        listRow = self._sendRequest(TablePlanetsRequestBuilder().getPlanetsInfoRequest(planetsNamesList))
        dictRow = self._unifyRow(listRow)
        for rowList in dictRow.itervalues():
            planetsList.append(Planet(*self._cleanRow(rowList, [9])))

        return planetsList

    def getSpeciesInfo(self, speciesNameList, completeInfo=True):
        """Method letting to retrieve data of species table.

        :param speciesNameList: the row the user wants to retrieve. If None, all row are retrieved.
        :param completeInfo: boolean indicating if we want to retrieve all columns and just minimal.
        :return: list of Specie instance.
        """
        speciesList = []

        listRow = self._sendRequest(TableSpeciesRequestBuilder().getSpeciesInfoRequest(speciesNameList, completeInfo))
        dictRow = self._unifyRow(listRow)
        for rowList in dictRow.itervalues():
            if completeInfo:
                r = self._cleanRow(rowList, [10, 11])
            else:
                r = self._cleanRow(rowList, [])
            speciesList.append(Specie(*r))

        return speciesList

