# !/usr/bin/env python
# -*- coding: utf-8 -*-

from defines import TablePeople, TableStarShips, TableVehicles, TablePeopleStarShips, TablePeopleVehicles, \
    TableFilmsPlanets, TablePeopleSpecies, TableFilms, TableSpecies, TablePlanets, TableFilmsSpecies, \
    TableFilmsPeoples, TableFilmsStarShips, TableFilmsVehicles


class RequestBuilder(object):
    """
    Abstract class letting to build request (build only the request (the str), but does not send it to the data base).
    """
    def __init__(self, tableId):
        super(RequestBuilder, self).__init__()
        self._tableId = tableId

    def _getSelectPart(self, attributesList, countAttribute=False):
        """Build the SELECT part of a request.

        :param attributesList: the attribute we want to retrieve -
        list of tuple [(tableId, [columnName1, columnName2, ...]), ...].
        :param countAttribute: boolean indicating if we want to count the rows.
        :return: partial request - str.
        """
        request = "SELECT"
        if attributesList:
            for tableId, attributesList in attributesList:
                for attibute in attributesList:
                    request += " {}.{}, ".format(tableId, attibute)
            request = request[:-2]

        if countAttribute:
            request += " COUNT(*)"
        return request

    def _getWherePart(self, attributesDict, associateConditions):
        """Build the WHERE part of a request.

        :param attributesDict: the attribute we want to retrieve -
        list of tuple {tableId: [(columnName1, [values1, values2]), ...], ...}.
        :param associateConditions: boolean indicating if the several conditions are with 'and' or 'or'.
        For more complicated case, please redefine method.
        :return: partial request - str.
        """
        conditionsSeparateWords = "or" if not associateConditions else "and"

        request = " WHERE"
        for tableId, attributesList in attributesDict.iteritems():
            for attibuteId, valuesList in attributesList:
                for v in valuesList:
                    request += " {}.{}='{}' {}".format(tableId, attibuteId, v, conditionsSeparateWords)
        request = request[:-len(conditionsSeparateWords)]
        return request

    def _getFromPart(self):
        """Return FROM part of a request.

        :return: partial request - str.
        """
        return " FROM {} ".format(self._tableId)

    def getCountRowTableRequest(self):
        """Count rows in a table.

        :return: Return the numbers of row in the table - int.
        """
        req = self._getSelectPart([], countAttribute=True)
        req += self._getFromPart()
        return req

    def _getInsertRowRequest(self, dictValues):
        """Return INSERT part of a request.

        :param dictValues: the values of the new row - {column1: value1, ...}
        :return: partial request - str.
        """
        request = 'INSERT INTO "{}" ('.format(self._tableId)

        for k in dictValues.iterkeys():
            request += ' "{}", '.format(k)
        request = request[:-2]

        request += ") VALUES ("
        for k in dictValues.itervalues():
            request += ' "{}", '.format(k)
        request = request[:-2]
        request += ")"

        return request

    def _getUpdateRowRequest(self, newData):
        """Return the UPDATE part of a request.

        :param newData: the new data - {column1: value1, ...}.
        :return: partial request - str.
        """
        request = "UPDATE {} SET".format(self._tableId)

        for k, val in newData.iteritems():
            request += " {}='{}',".format(k, val)
        request = request[:-1]
        return request

    def _getDeleteRowRequest(self, dictConditions, associateConditions):
        """Delete a row from a table.

        :param dictConditions: conditions to select the row to remove - {Column1 : value1, ...}.
        :param associateConditions: boolean indicating if the several conditions are with 'and' or 'or'.
        For more complicated case, please redefine method.
        :return: partial request - str.
        """
        conditionsSeparateWords = "or" if not associateConditions else "and"

        request = 'DELETE FROM "{}" WHERE'.format(self._tableId)

        for k, v in dictConditions.iteritems():
            request += ' {}="{}" {}'.format(k, v, conditionsSeparateWords)
        request = request[:-len(conditionsSeparateWords)]

        return request


class TablePeopleRequestBuilder(RequestBuilder):
    """
    Class letting to build request for people table.
    """
    def __init__(self):
        super(TablePeopleRequestBuilder, self).__init__(TablePeople.ID)

    def getPeoplesInfoRequest(self, personNameList):
        """Return request for retrieving data in people table.

        :param personNameList: the specific row we want to eventually retrieved. Can be None.
        If it is None, we retrieve all the row of the table.
        :return: the complete request - str.
        """
        infoToGet = [(TablePeople.ID, [TablePeople.COLUMN_ID, TablePeople.COLUMN_NAME, TablePeople.COLUMN_HEIGHT,
                                       TablePeople.COLUMN_MASS, TablePeople.COLUMN_HAIR_COLOR,
                                       TablePeople.COLUMN_SKIN_COLOR, TablePeople.COLUMN_EYE_COLOR,
                                       TablePeople.COLUMN_BIRTH_YEAR, TablePeople.COLUMN_GENDER,
                                       TablePeople.COLUMN_HOME_WORLD, TablePeople.COLUMN_DATE_CREATED,
                                       TablePeople.COLUMN_DATA_EDITED]),
                     (TableVehicles.ID, [TableVehicles.COLUMN_NAME]),
                     (TableStarShips.ID, [TableStarShips.COLUMN_NAME]),
                     (TableFilms.ID, [TableFilms.COLUMN_TITLE]),
                     (TableSpecies.ID, [TableSpecies.COLUMN_NAME])]
        request = self._getSelectPart(infoToGet)

        # request += ", GROUP_CONCAT(DISTINCT starships.name), GROUP_CONCAT(DISTINCT vehicles.name)" => bug for all
        request += self._getFromPart()

        request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TablePeopleStarShips.ID,
                                                           TablePeopleStarShips.ID, TablePeopleStarShips.COLUMN_PEOPLE,
                                                           TablePeople.ID, TablePeople.COLUMN_ID)
        request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableStarShips.ID,
                                                           TableStarShips.ID, TableStarShips.COLUMN_ID,
                                                           TablePeopleStarShips.ID,
                                                           TablePeopleStarShips.COLUMN_STAR_SHIPS)

        request += " LEFT JOIN {} ON {}.{} = {}.id".format(TablePeopleVehicles.ID,
                                                           TablePeopleVehicles.ID, TablePeopleVehicles.COLUMN_PEOPLE,
                                                           TablePeople.ID, TablePeople.COLUMN_ID)
        request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableVehicles.ID,
                                                           TableVehicles.ID, TableVehicles.COLUMN_ID,
                                                           TablePeopleVehicles.ID, TablePeopleVehicles.COLUMN_VEHICLES)

        request += " LEFT JOIN {} ON {}.{} = {}.id".format(TableFilmsPeoples.ID,
                                                           TableFilmsPeoples.ID, TableFilmsPeoples.COLUMN_PEOPLE,
                                                           TablePeople.ID, TablePeople.COLUMN_ID)
        request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableFilms.ID,
                                                           TableFilms.ID, TableFilms.COLUMN_ID,
                                                           TableFilmsPeoples.ID, TableFilmsPeoples.COLUMN_FILMS)

        request += " LEFT JOIN {} ON {}.{} = {}.id".format(TablePeopleSpecies.ID,
                                                           TablePeopleSpecies.ID, TablePeopleSpecies.COLUMN_PEOPLE,
                                                           TablePeople.ID, TablePeople.COLUMN_ID)
        request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableSpecies.ID,
                                                           TableSpecies.ID, TableSpecies.COLUMN_ID,
                                                           TablePeopleSpecies.ID, TablePeopleSpecies.COLUMN_SPECIES)
        if personNameList:
            request += self._getWherePart({TablePeople.ID: [(TablePeople.COLUMN_NAME, personNameList)]}, False)

        return request

    def getInsertRowRequest(self, peopleObject):
        """Return request for adding new row in people table.

        :param peopleObject: People instances where the of the new row are registered.
        :return: the complete request - str.
        """
        dictValues = {TablePeople.COLUMN_NAME: peopleObject.getName(),
                      TablePeople.COLUMN_HEIGHT: peopleObject.getHeight(),
                      TablePeople.COLUMN_MASS: peopleObject.getMass(),
                      TablePeople.COLUMN_HAIR_COLOR: peopleObject.getHairColor(),
                      TablePeople.COLUMN_SKIN_COLOR: peopleObject.getSkinColor(),
                      TablePeople.COLUMN_EYE_COLOR: peopleObject.getEyeColor(),
                      TablePeople.COLUMN_BIRTH_YEAR: peopleObject.getBirthYear(),
                      TablePeople.COLUMN_GENDER: peopleObject.getGender(),
                      TablePeople.COLUMN_DATE_CREATED: peopleObject.getDateCreated(),
                      TablePeople.COLUMN_DATA_EDITED: peopleObject.getDateEdited(),
                      TablePeople.COLUMN_ID: peopleObject.getId(),
                      TablePeople.COLUMN_URL: peopleObject.getId()}
        return self._getInsertRowRequest(dictValues)

    def getUpdatePeopleInfoRequest(self, peopleId, newData):
        """Return request for updating row in people table.

        :param peopleId: id of the people we want to update - primary key => modify only one row.
        :param newData: the new data for the people - {column1: value1, ...}.
        :return: the complete request - str.
        """
        request = self._getUpdateRowRequest(newData)
        request += self._getWherePart({TablePeople.ID: [(TablePeople.COLUMN_ID, peopleId)]}, False)

        return request

    def getDeleteRequest(self, peopleId):
        """Return request for deleting row in people table.

        :param peopleId: id of the people we want to delete - primary key => delete only one row.
        :return: the complete request - str.
        """
        return self._getDeleteRowRequest({TablePeople.COLUMN_ID: peopleId}, True)


class TableVehiclesRequestBuilder(RequestBuilder):
    """
    Class letting to build request for vehicles table.
    """
    def __init__(self):
        super(TableVehiclesRequestBuilder, self).__init__(TableVehicles.ID)

    def getVehiclesInfoRequest(self, vehiclesNameList, completeInfo):
        """Return request for retrieving data in vehicle table.

        :param vehiclesNameList: the specific row we want to eventually retrieved. Can be None.
        If it is None, we retrieve all the row of the table.
        :param completeInfo: boolean indicating if we want to retrieve all columns or just minimal.
        :return: the complete request - str.
        """
        if completeInfo:
            infoToGet = [(TableVehicles.ID, [TableVehicles.COLUMN_ID, TableVehicles.COLUMN_NAME,
                                             TableVehicles.COLUMN_MODEL, TableVehicles.COLUMN_MANUFACTURER,
                                             TableVehicles.COLUMN_COST, TableVehicles.COLUMN_LENGTH,
                                             TableVehicles.COLUMN_MAX_SPEED, TableVehicles.COLUMN_CREW,
                                             TableVehicles.COLUMN_PASSENGERS, TableVehicles.COLUMN_CARGO_CAPACITY,
                                             TableVehicles.COLUMN_CONSUMABLES, TableVehicles.COLUMN_VEHICLE_CLASS])]
        else:
            infoToGet = [(TableVehicles.ID, [TableVehicles.COLUMN_ID, TableVehicles.COLUMN_NAME])]

        req = self._getSelectPart(infoToGet)
        req += self._getFromPart()
        if vehiclesNameList:
            req += self._getWherePart({TableVehicles.ID: [(TableVehicles.COLUMN_NAME, vehiclesNameList)]}, False)

        return req


class TableStarShipsRequestBuilder(RequestBuilder):
    """
    Class letting to build request for vehicles table.
    """
    def __init__(self):
        super(TableStarShipsRequestBuilder, self).__init__(TableStarShips.ID)

    def getStarShipsInfoRequest(self, starShipsNameList, completeInfo):
        """Return request for retrieving data in vehicle table.

        :param starShipsNameList: the specific row we want to eventually retrieved. Can be None.
        If it is None, we retrieve all the row of the table.
        :param completeInfo: boolean indicating if we want to retrieve all columns or just minimal.
        :return: the complete request - str.
        """
        if completeInfo:
            infoToGet = [(TableStarShips.ID, [TableStarShips.COLUMN_ID, TableStarShips.COLUMN_NAME,
                                              TableStarShips.COLUMN_MODEL, TableStarShips.COLUMN_MANUFACTURER,
                                              TableStarShips.COLUMN_COST, TableStarShips.COLUMN_LENGTH,
                                              TableStarShips.COLUMN_MAX_SPEED, TableStarShips.COLUMN_CREW,
                                              TableStarShips.COLUMN_PASSENGERS, TableStarShips.COLUMN_CARGO_CAPACITY,
                                              TableStarShips.COLUMN_CONSUMABLES, TableStarShips.COLUMN_HYPERDRIVE_RATING,
                                              TableStarShips.COLUMN_MGLT, TableStarShips.COLUMN_STAR_SHIP_CLASS])]
        else:
            infoToGet = [(TableStarShips.ID, [TableStarShips.COLUMN_ID, TableStarShips.COLUMN_NAME])]

        req = self._getSelectPart(infoToGet)
        req += self._getFromPart()
        if starShipsNameList:
            req += self._getWherePart({TableStarShips.ID: [(TableStarShips.COLUMN_NAME, starShipsNameList)]}, False)

        return req


class TablePeopleStarShipsRequestBuilder(RequestBuilder):
    """
    Class letting to build request for starships-people table.
    """
    def __init__(self):
        super(TablePeopleStarShipsRequestBuilder, self).__init__(TablePeopleStarShips.ID)

    def getInsertRowRequest(self, idPeople, idStarShip):
        """Return INSERT part of a request.

        :param idPeople: id of the column people of the new row  - str.
        :param idStarShip: id of the column starships of the new row  - str.
        :return: partial request - str.
        """
        dictValues = {TablePeopleStarShips.COLUMN_PEOPLE: idPeople,
                      TablePeopleStarShips.COLUMN_STAR_SHIPS: idStarShip}
        return self._getInsertRowRequest(dictValues)

    def getDeleteRowRequest(self, idPeople, idStarShip):
        """Return request for deleting row in people starsips-people table.

        :param idPeople: id of the people column we want to delete - str.
        :param idStarShip: id of the starships column we want to delete - str.
        :return: the complete request - str.
        """
        dictConditions = {TablePeopleStarShips.COLUMN_PEOPLE: idPeople,
                          TablePeopleStarShips.COLUMN_STAR_SHIPS: idStarShip}

        return self._getDeleteRowRequest(dictConditions, True)


class TablePeopleVehiclesRequestBuilder(RequestBuilder):
    """
    Class letting to build request for vehicles-people table.
    """
    def __init__(self):
        super(TablePeopleVehiclesRequestBuilder, self).__init__(TablePeopleVehicles.ID)

    def getInsertRowRequest(self, idPeople, idVehicle):
        """Return INSERT part of a request.

        :param idPeople: id of the column people of the new row  - str.
        :param idVehicle: id of the column vehicles of the new row  - str.
        :return: partial request - str.
        """
        dictValues = {TablePeopleVehicles.COLUMN_PEOPLE: idPeople,
                      TablePeopleVehicles.COLUMN_VEHICLES: idVehicle}
        return self._getInsertRowRequest(dictValues)

    def getDeleteRowRequest(self, idPeople, idVehicle):
        """Return request for deleting row in people starsips-people table.

        :param idPeople: id of the people column we want to delete - str.
        :param idVehicle: id of the vehicles column we want to delete - str.
        :return: the complete request - str.
        """
        dictConditions = {TablePeopleVehicles.COLUMN_PEOPLE: idPeople,
                          TablePeopleVehicles.COLUMN_VEHICLES: idVehicle}

        return self._getDeleteRowRequest(dictConditions, True)


class TableFilmsPeopleRequestBuilder(RequestBuilder):
    """
    Class letting to build request for films-people table.
    """
    def __init__(self):
        super(TableFilmsPeopleRequestBuilder, self).__init__(TableFilmsPeoples.ID)

    def getInsertRowRequest(self, idPeople, idFilm):
        """Return INSERT part of a request.

        :param idPeople: id of the column people of the new row  - str.
        :param idFilm: id of the column films of the new row  - str.
        :return: partial request - str.
        """
        dictValues = {TableFilmsPeoples.COLUMN_PEOPLE: idPeople,
                      TableFilmsPeoples.COLUMN_FILMS: idFilm}
        return self._getInsertRowRequest(dictValues)


class TablePeopleSpeciesRequestBuilder(RequestBuilder):
    """
    Class letting to build request for species-people table.
    """
    def __init__(self):
        super(TablePeopleSpeciesRequestBuilder, self).__init__(TablePeopleSpecies.ID)

    def getInsertRowRequest(self, idPeople, idSpecie):
        """Return INSERT part of a request.

        :param idPeople: id of the column people of the new row  - str.
        :param idSpecie: id of the column species of the new row  - str.
        :return: partial request - str.
        """
        dictValues = {TablePeopleSpecies.COLUMN_PEOPLE: idPeople,
                      TablePeopleSpecies.COLUMN_SPECIES: idSpecie}
        return self._getInsertRowRequest(dictValues)


class TableFilmsRequestBuilder(RequestBuilder):
    """
    Class letting to build request for films table.
    """
    def __init__(self):
        super(TableFilmsRequestBuilder, self).__init__(TableFilms.ID)

    def getFilmsInfoRequest(self, filmsNameList, completeInfo):
        """Return request for retrieving data in films table.

        :param filmsNameList: the specific row we want to eventually retrieved. Can be None.
        If it is None, we retrieve all the row of the table.
        :param completeInfo: boolean indicating if we want to retrieve all columns or just minimal.
        :return: the complete request - str.
        """
        if completeInfo:
            infoToGet = [(TableFilms.ID, [TableFilms.COLUMN_ID, TableFilms.COLUMN_TITLE, TableFilms.COLUMN_EPISODE_ID,
                                          TableFilms.COLUMN_OPENING_CRAWL, TableFilms.COLUMN_DIRECTOR,
                                          TableFilms.COLUMN_PRODUCER, TableFilms.COLUMN_RELEASE_DATE]),
                         (TablePeople.ID, [TablePeople.COLUMN_NAME]),
                         (TablePlanets.ID, [TablePlanets.COLUMN_NAME]),
                         (TableStarShips.ID, [TableStarShips.COLUMN_NAME]),
                         (TableVehicles.ID, [TableVehicles.COLUMN_NAME]),
                         (TableSpecies.ID, [TableSpecies.COLUMN_NAME])]
        else:
            infoToGet = [(TableFilms.ID, [TableFilms.COLUMN_ID, TableFilms.COLUMN_TITLE])]

        request = self._getSelectPart(infoToGet)
        request += self._getFromPart()

        if completeInfo:
            request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableFilmsPeoples.ID,
                                                               TableFilmsPeoples.ID, TableFilmsPeoples.COLUMN_FILMS,
                                                               TableFilms.ID, TableFilms.COLUMN_ID)
            request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TablePeople.ID,
                                                               TablePeople.ID, TablePeople.COLUMN_ID,
                                                               TableFilmsPeoples.ID, TableFilmsPeoples.COLUMN_PEOPLE)

            request += " LEFT JOIN {} ON {}.{} = {}.id".format(TableFilmsPlanets.ID,
                                                               TableFilmsPlanets.ID, TableFilmsPlanets.COLUMN_FILM,
                                                               TableFilms.ID, TableFilms.COLUMN_ID)
            request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TablePlanets.ID,
                                                               TablePlanets.ID, TablePlanets.COLUMN_ID,
                                                               TableFilmsPlanets.ID, TableFilmsPlanets.COLUMN_PLANET)

            request += " LEFT JOIN {} ON {}.{} = {}.id".format(TableFilmsStarShips.ID,
                                                               TableFilmsStarShips.ID, TableFilmsStarShips.COLUMN_FILMS,
                                                               TableFilms.ID, TableFilms.COLUMN_ID)
            request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableStarShips.ID,
                                                               TableStarShips.ID, TableStarShips.COLUMN_ID,
                                                               TableFilmsStarShips.ID,
                                                               TableFilmsStarShips.COLUMN_STAR_SHIPS)

            request += " LEFT JOIN {} ON {}.{} = {}.id".format(TableFilmsVehicles.ID,
                                                               TableFilmsVehicles.ID, TableFilmsVehicles.COLUMN_FILMS,
                                                               TableFilms.ID, TableFilms.COLUMN_ID)
            request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableVehicles.ID,
                                                               TableVehicles.ID, TableVehicles.COLUMN_ID,
                                                               TableFilmsVehicles.ID, TableFilmsVehicles.COLUMN_VEHICLES)

            request += " LEFT JOIN {} ON {}.{} = {}.id".format(TableFilmsSpecies.ID,
                                                               TableFilmsSpecies.ID, TableFilmsSpecies.COLUMN_FILMS,
                                                               TableFilms.ID, TableFilms.COLUMN_ID)
            request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableSpecies.ID,
                                                               TableSpecies.ID, TableSpecies.COLUMN_ID,
                                                               TableFilmsSpecies.ID, TableFilmsSpecies.COLUMN_SPECIES)

        if filmsNameList:
            request += self._getWherePart({TableFilms.ID: [(TableFilms.COLUMN_TITLE, filmsNameList)]}, False)

        return request


class TableSpeciesRequestBuilder(RequestBuilder):
    """
    Class letting to build request for species table.
    """
    def __init__(self):
        super(TableSpeciesRequestBuilder, self).__init__(TableSpecies.ID)

    def getSpeciesInfoRequest(self, speciesNameList, completeInfo):
        """Return request for retrieving data in species table.

        :param speciesNameList: the specific row we want to eventually retrieved. Can be None.
        If it is None, we retrieve all the row of the table.
        :param completeInfo: boolean indicating if we want to retrieve all columns or just minimal.
        :return: the complete request - str.
        """
        if completeInfo:
            infoToGet = [(TableSpecies.ID, [TableSpecies.COLUMN_NAME, TableSpecies.COLUMN_CLASSIFICATION,
                                            TableSpecies.COLUMN_DESIGNATION, TableSpecies.COLUMN_AVERAGE_HEIGHT,
                                            TableSpecies.COLUMN_SKIN_COORS, TableSpecies.COLUMN_HAIR_COLORS,
                                            TableSpecies.COLUMN_EYE_COLORS, TableSpecies.COLUMN_AVERAGE_LIFE_SPAN,
                                            TableSpecies.COLUMN_HOME_WORLD, TableSpecies.COLUMN_LANGUAGE]),
                         (TablePeople.ID, [TablePeople.COLUMN_NAME]),
                         (TableFilms.ID, [TableFilms.COLUMN_TITLE])]
        else:
            infoToGet = [(TableSpecies.ID, [TableSpecies.COLUMN_ID, TableSpecies.COLUMN_NAME])]

        request = self._getSelectPart(infoToGet)
        request += self._getFromPart()

        if completeInfo:
            request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TablePeopleSpecies.ID,
                                                               TablePeopleSpecies.ID, TablePeopleSpecies.COLUMN_SPECIES,
                                                               TableSpecies.ID, TableSpecies.COLUMN_ID)
            request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TablePeople.ID,
                                                               TablePeople.ID, TablePeople.COLUMN_ID,
                                                               TablePeopleSpecies.ID, TablePeopleSpecies.COLUMN_PEOPLE)
            request += " LEFT JOIN {} ON {}.{} = {}.id".format(TableFilmsSpecies.ID,
                                                               TableFilmsSpecies.ID, TableFilmsSpecies.COLUMN_FILMS,
                                                               TableSpecies.ID, TableSpecies.COLUMN_ID)
            request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableFilms.ID,
                                                               TableFilms.ID, TableFilms.COLUMN_ID,
                                                               TableFilmsSpecies.ID, TableFilmsSpecies.COLUMN_SPECIES)

        if speciesNameList:
            request += self._getWherePart({TableSpecies.ID: [(TableSpecies.COLUMN_NAME, speciesNameList)]}, False)

        return request


class TablePlanetsRequestBuilder(RequestBuilder):
    """
    Class letting to build request for planets table.
    """
    def __init__(self):
        super(TablePlanetsRequestBuilder, self).__init__(TablePlanets.ID)

    def getPlanetsInfoRequest(self, planetsNameList):
        """Return request for retrieving data in planets table.

        :param planetsNameList: the specific row we want to eventually retrieved. Can be None.
        If it is None, we retrieve all the row of the table.
        :return: the complete request - str.
        """
        infoToGet = [(TablePlanets.ID, [TablePlanets.COLUMN_NAME, TablePlanets.COLUMN_ROTATION_PERIOD,
                                        TablePlanets.COLUMN_ORBITAL_PERIOD, TablePlanets.COLUMN_DIAMETER,
                                        TablePlanets.COLUMN_CLIMATE, TablePlanets.COLUMN_GRAVITY,
                                        TablePlanets.COLUMN_TERRAIN, TablePlanets.COLUMN_SURFACE_WATER,
                                        TablePlanets.COLUMN_POPULATION]),
                     (TableFilms.ID, [TableFilms.COLUMN_TITLE])]

        request = self._getSelectPart(infoToGet)
        request += self._getFromPart()

        request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableFilmsPlanets.ID,
                                                           TableFilmsPlanets.ID, TableFilmsPlanets.COLUMN_PLANET,
                                                           TablePlanets.ID, TablePlanets.COLUMN_ID)
        request += " LEFT JOIN {} ON {}.{} = {}.{}".format(TableFilms.ID,
                                                           TableFilms.ID, TableFilms.COLUMN_ID,
                                                           TableFilmsPlanets.ID, TableFilmsPlanets.COLUMN_FILM)

        if planetsNameList:
            request += self._getWherePart({TablePlanets.ID: [(TablePlanets.COLUMN_NAME, planetsNameList)]}, False)

        return request
