# !/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import datetime
import data_base_manager
import people
from defines import TablePeople, TableStarShips, TableSpecies, TableVehicles, TablePlanets, TableFilms


class Application(object):
    """
    Class corresponding to the controller of the application.
    All actions desired by the user has captured here and then the associated action are run.
    """
    def __init__(self, dataFilePath):
        super(Application, self).__init__()

        self._dataBaseManager = data_base_manager.DataBaseManager()
        self._dataBaseManager.openConnection(dataFilePath)

    def startApp(self):
        """Start application method.

        :return: None.
        """
        manual = "What do you want to do ?\n" \
                 "1 - Display people info\n" \
                 "2 - Add new people\n" \
                 "3 - Update people info\n" \
                 "4 - Delete a people\n" \
                 "5 - Get info in others tables\n" \
                 "6 - Close program\n\n"

        toContinue = True
        while toContinue:
            x = raw_input(manual)
            if x == '1':
                self._displayingTableInfo(TablePeople.ID)
            elif x == '2':
                self._addingNewPeopleMode()
            elif x == '3':
                self._updatingPeopleInfoMode()
            elif x == '4':
                self._deletingPeopleMode()
            elif x == '5':
                self._displayInfoMode()
            elif x == '6':
                self._closeApp()
                toContinue = False

    def _displayInfoMode(self):
        """Method letting to choice on which table the user want to retrieve data..

        :return: None.
        """
        manual = "In which table do you want info ?\n" \
                 "1 - People\n" \
                 "2 - Species\n" \
                 "3 - Films\n" \
                 "4 - Planets\n" \
                 "5 - Vehicles\n" \
                 "6 - Starships\n" \
                 "7 - Back to the previous menu\n\n"

        toContinue = True
        tableId = ""
        while toContinue:
            x = raw_input(manual)
            if x == '1':
                tableId = TablePeople.ID
            elif x == '2':
                tableId = TableSpecies.ID
            elif x == '3':
                tableId = TableFilms.ID
            elif x == '4':
                tableId = TablePlanets.ID
            elif x == '5':
                tableId = TableVehicles.ID
            elif x == '5':
                tableId = TableStarShips.ID
            elif x == '7':
                toContinue = False
                continue
            self._displayingTableInfo(tableId)

    def _getInfo(self, tableId, rowNames=None):
        """Retrieve the info on the table "tableId".

        :param tableId: str, correspond to the Id of a data base table.
        :param rowNames: list precising on which row we want to retrieve data - list[str].
        Can be None (retrieve all data in this case).
        :return: list of objects instances where the data are saved.
        """
        if tableId == TablePeople.ID:
            return self._dataBaseManager.getPeopleInfo(rowNames)
        elif tableId == TableFilms.ID:
            return self._dataBaseManager.getFilmsInfo(rowNames)
        elif tableId == TablePlanets.ID:
            return self._dataBaseManager.getPlanetsInfo(rowNames)
        elif tableId == TableSpecies.ID:
            return self._dataBaseManager.getSpeciesInfo(rowNames)
        elif tableId == TableStarShips.ID:
            return self._dataBaseManager.getStarShipsInfo(rowNames)
        elif tableId == TableVehicles.ID:
            return self._dataBaseManager.getVehiclesInfo(rowNames)

    def _getObjectInstanceName(self, objectInstance, tableId):
        """Return the "visible" id of a objectInstance => the name.

        :param objectInstance: instance of a class representing a data base table row
        (Planet, Specie, StarShip, Vehicle, People, Film).
        :param tableId: id of the table associated to the data - str.
        :return:
        """
        if tableId == TablePeople.ID:
            return objectInstance.getName()
        elif tableId == TableFilms.ID:
            return objectInstance.getTitle()
        elif tableId == TablePlanets.ID:
            return objectInstance.getName()
        elif tableId == TableSpecies.ID:
            return objectInstance.getName()
        elif tableId == TableStarShips.ID:
            return objectInstance.getName()
        elif tableId == TableVehicles.ID:
            return objectInstance.getName()

    def _displayingTableInfo(self, tableId):
        """Method letting to retrieve and display data from data base.
        The user can also precise some info in order to filter the rows he wants to display.

        :param tableId: the id of the table on which we will work - str.
        :return: None.
        """
        manual = "Enter the names of data for which you want info.\n" \
                 "Finish the list by an empty names.\n" \
                 "To display all data info, enter only * and validate.\n"
        if tableId == TableFilms.ID:
            manual += "Warning, display all info about films will take very long time."
        manual += "To come back to previous mode, enter a empty list.\n\n"

        toContinue = True
        listNames = []
        while toContinue:
            x = raw_input(manual)
            if x == '':
                if listNames:
                    if len(listNames) == 1 and listNames[0] == "*":
                        for p in self._getInfo(tableId):
                            print p, "\n"
                    else:
                        dictInfo = {}
                        for p in self._getInfo(tableId, listNames):
                            objName = self._getObjectInstanceName(p, tableId)
                            listPeople = dictInfo.get(objName, [])
                            listPeople.append(p)
                            if len(listPeople) == 1:
                                dictInfo[objName] = listPeople

                        for nameAsking in listNames:
                            if nameAsking in dictInfo:
                                for p in dictInfo[nameAsking]:
                                    print p
                                    print "\n"
                            else:
                                print 'None info found for name {}'.format(nameAsking)
                        print "\n"
                else:
                    toContinue = False
                listNames = []
            else:
                if "'" in x or '"' in x:
                    print "{} or {} characters can not be in name people".format("'", '"')
                else:
                    listNames.append(x)

    def _addingNewPeopleMode(self):
        """Method letting to the user to create a new row in the people table and add it in it.
        The user can precise all fields of the new people.
        Once satisfied, he can add this new row in the table.

        :return:
        """
        manual = "Enter info about this new people.\n" \
                 "Careful, for starships and vehicles, insert only comma between names of starships/vehicles " \
                 "(not any space)"
        infoToGet = OrderedDict([("name", ""), ("height", ""), ("mass", ""), ("hair color", ""), ("skin color", ""),
                                 ("eye color", ""), ("birth day", ""), ("gender", ""), ("homeworld", ""),
                                 ("starships names", [""]), ("vehicles names", [""]), ("films names", [""]),
                                 ("species names", [""])])

        print manual
        for infoDesc in infoToGet.keys():
            x = raw_input(infoDesc + ": \n")
            if infoDesc in ["starships names", "vehicles names", "films names", "species names"]:
                if x == "":
                    x = []
                else:
                    x = x.split(",")
            elif infoDesc == "name":
                if x == "":
                    x = raw_input("Name value can not be empty. Please enter a value.\n"
                                  "If a new empty value is entered, we will return to the previous mode.\n")
                    if x == "":
                        return
            elif "'" in x or '"' in x:
                print "{} or {} characters can not be in entry".format("'", '"')
                print "Operation canceled"
                return
            infoToGet[infoDesc] = x

        idPeople = self._dataBaseManager.getNewIdPeople()
        dateCreated = datetime.datetime.utcnow()
        newPeople = people.People(idPeople, infoToGet["name"], infoToGet["height"], infoToGet["mass"],
                                  infoToGet["hair color"], infoToGet["skin color"], infoToGet["eye color"],
                                  infoToGet["birth day"], infoToGet["gender"], infoToGet["homeworld"],
                                  dateCreated, dateCreated, infoToGet["vehicles names"], infoToGet["starships names"],
                                  infoToGet["films names"], infoToGet["species names"])
        # add new row in people table.
        self._dataBaseManager.addNewPeople(newPeople)

        # add new row in starhips-people table.
        starShipsNames = newPeople.getStarShips()
        if starShipsNames:
            starShipsFound = self._dataBaseManager.getStarShipsInfo(starShipsNames, False)
            for starShip in starShipsFound:
                self._dataBaseManager.addStarShipToPeople(idPeople, starShip.getId())
                starShipsNames.remove(starShip.getName())
            if starShipsNames:
                print "The following star ships have not been found. There are not been added in the new people."
            for starShipsName in starShipsNames:
                print starShipsName,
            print

        # add new row in vehicles-people table.
        vehiclesNames = newPeople.getVehicles()
        if vehiclesNames:
            vehiclesFound = self._dataBaseManager.getVehiclesInfo(vehiclesNames, False)
            for vehicle in vehiclesFound:
                self._dataBaseManager.addVehicleToPeople(idPeople, vehicle.getId())
                vehiclesNames.remove(vehicle.getName())
            if vehiclesNames:
                print "The following vehicles have not been found. There are not been added in the new people."
            for vehiclesName in vehiclesNames:
                print vehiclesName,
            print

        # add new row in films-people table.
        filmsNames = newPeople.getFilms()
        if filmsNames:
            filmsFound = self._dataBaseManager.getFilmsInfo(filmsNames, False)
            for film in filmsFound:
                self._dataBaseManager.addFilmsToPeople(idPeople, film.getId())
                filmsNames.remove(film.getTitle())
            if filmsNames:
                print "The following films have not been found. There are not been added in the new people."
            for filmName in filmsNames:
                print filmName,
            print

        # add new row in species-people table.
        speciesNames = newPeople.getSpecies()
        if speciesNames:
            speciesFound = self._dataBaseManager.getSpeciesInfo(speciesNames, False)
            for specie in speciesFound:
                self._dataBaseManager.addSpecieToPeople(idPeople, specie.getId())
                speciesNames.remove(specie.getName())
            if speciesNames:
                print "The following species have not been found. There are not been added in the new people."
            for specieName in speciesNames:
                print specieName,
            print

    def _updatingPeopleInfoMode(self):
        """Method letting to choice a people on which the user wants to update data.

        :return: None.
        """
        manual = "Enter the name of the people you want to update the info.\n" \
                 "To come back to previous mode, enter a empty data.\n\n"

        toContinue = True
        while toContinue:
            x = raw_input(manual)
            if x == "":
                toContinue = False
            elif x == "*":
                print "* is not available here"
            elif "'" in x or '"' in x:
                print "{} or {} characters can not be in name people".format("'", '"')
            else:
                peopleInfoList = self._dataBaseManager.getPeopleInfo([x])
                if len(peopleInfoList) == 0:
                    print "People has not been found."
                    continue

                if len(peopleInfoList) != 1:
                    print "There are several possible people with the name given"
                    try:
                        pNumber = self._choicePeopleFromList(x, peopleInfoList)
                    except ValueError:
                        print 'pNumber is not valid'
                        continue
                    else:
                        peopleInfo = peopleInfoList[pNumber]
                else:
                    peopleInfo = peopleInfoList[0]
                self._updatePeopleData(peopleInfo)

    def _updatePeopleData(self, peopleInfo):
        """Method letting to update the data of a row in the people table (the user has already chosen
        the row in the calling method).

        :param peopleInfo: People instance - correspond to the row table that the user want to update.
        :return: None.
        """
        def _updateListData(idData, state, newElt):
            """Update the value of "complex" data (starShips list, vehicles...).

            :param idData: id of the associate column of the data in the table - str.
            :param state: indicate if the data is added or removed - int.
            :param newElt: the new data or data to remove.
            :return: None.
            """
            dictData = newData.get(idData, {})
            isNewDict = len(dictData) == 0
            listData = dictData.get(state, [])
            otherStateListData = dictData.get(0 if state == 1 else 1, [])
            if newElt not in otherStateListData:
                listData.append(newElt)
                if len(listData):
                    dictData[state] = listData
                    if isNewDict:
                        newData[idData] = dictData
            else:
                otherStateListData.remove(newElt)

        toContinue = True
        newData = {}

        while toContinue:
            manual = "\nWhich info do you want to update ? " \
                     "(select one, update it and select another one if you want)\n"
            manual += "1 - name\n" \
                      "2 - height\n" \
                      "3 - mass\n" \
                      "4 - hair color\n" \
                      "5 - skin color\n" \
                      "6 - eye color\n" \
                      "7 - birth day\n" \
                      "8 - gender\n" \
                      "9 - homeworld\n" \
                      "10 - starships names\n" \
                      "11 - vehicles names\n" \
                      "12 - commit changes\n" \
                      "13 - display actual people info " \
                      "(with the modifications already asked (but not commited in data base)\n" \
                      "14 - cancel\n" \
                      "(Careful, if you do not commit the modifications, there will be not saved)\n"

            y = raw_input(manual)
            if "'" in y or '"' in y:
                print "{} or {} characters can not be in entry".format("'", '"')
            else:
                if y == '1':
                    newHeight = raw_input("Enter the new value\n")
                    newData[TablePeople.COLUMN_NAME] = newHeight
                    peopleInfo.setName(newHeight)
                elif y == '2':
                    newHeight = raw_input("Enter the new value\n")
                    newData[TablePeople.COLUMN_HEIGHT] = newHeight
                    peopleInfo.setHeight(newHeight)
                elif y == '3':
                    newMass = raw_input("Enter the new value\n")
                    newData[TablePeople.COLUMN_MASS] = newMass
                    peopleInfo.setMass(newMass)
                elif y == '4':
                    newHairColor = raw_input("Enter the new value\n")
                    newData[TablePeople.COLUMN_HAIR_COLOR] = newHairColor
                    peopleInfo.setHairColor(newHairColor)
                elif y == '5':
                    newSkinColor = raw_input("Enter the new value\n")
                    newData[TablePeople.COLUMN_SKIN_COLOR] = newSkinColor
                    peopleInfo.setSkinColor(newSkinColor)
                elif y == '6':
                    newEyeColor = raw_input("Enter the new value\n")
                    newData[TablePeople.COLUMN_EYE_COLOR] = newEyeColor
                    peopleInfo.setEyeColor(newEyeColor)
                elif y == '7':
                    newBirthDay = raw_input("Enter the new value\n")
                    newData[TablePeople.COLUMN_BIRTH_YEAR] = newBirthDay
                    peopleInfo.setBirthDay(newBirthDay)
                elif y == '8':
                    newGender = raw_input("Enter the new value\n")
                    newData[TablePeople.COLUMN_GENDER] = newGender
                    peopleInfo.setGender(newGender)
                elif y == '9':
                    newHomeWorld = raw_input("Enter the new value\n")
                    newData[TablePeople.COLUMN_HOME_WORLD] = newHomeWorld
                    peopleInfo.setHomeWorld(newHomeWorld)
                elif y == '10':
                    z = raw_input("Choice what you want to do\n"
                                  "1 - add new star ship\n"
                                  "2 - remove a star ship\n")
                    if z == "1":
                        vehicleName = raw_input("Enter the new star ship name\n")
                        starShipData = self._dataBaseManager.getStarShipsInfo([vehicleName], False)
                        if len(starShipData) != 0:
                            if vehicleName not in peopleInfo.getStarShips():
                                peopleInfo.addStarShip(vehicleName)
                                _updateListData(TablePeople.COLUMN_STAR_SHIPS, 1, starShipData[0].getId())
                            else:
                                print "Star ship already added for this people. Not added.\n"
                        else:
                            print "Star ship does not exist. Not added.\n"
                    elif z == "2":
                        actualVehiclesNames = ""
                        for vehicleName in peopleInfo.getStarShips():
                            actualVehiclesNames += vehicleName + ", "
                        vehicleName = raw_input("Enter the name of the start ship to remove.\n"
                                                "Actual star ships names : {}\n".format(actualVehiclesNames))
                        starShipData = self._dataBaseManager.getStarShipsInfo([vehicleName], False)
                        if len(starShipData) != 0:
                            try:
                                peopleInfo.removeStarShip(vehicleName)
                            except ValueError:
                                print "star ship is not hold by this people. Not removed.\n"
                            else:
                                _updateListData(TablePeople.COLUMN_STAR_SHIPS, 0, starShipData[0].getId())
                        else:
                            print "Star ship does not exist. Not removed.\n"
                elif y == '11':
                    z = raw_input("Choice what you want to do\n"
                                  "1 - add new vehicle\n"
                                  "2 - remove a vehicle\n")
                    if z == "1":
                        vehicleName = raw_input("Enter the new vehicle name\n")
                        vehicleData = self._dataBaseManager.getVehiclesInfo([vehicleName], False)
                        if len(vehicleData) != 0:
                            if vehicleName not in peopleInfo.getVehicles():
                                peopleInfo.addVehicle(vehicleName)
                                _updateListData(TablePeople.COLUMN_VEHICLES, 1, vehicleData[0].getId())
                            else:
                                print "Star ship already added for this people. Not added.\n"
                        else:
                            print "Vehicle does not exist. Not added.\n"
                    elif z == "2":
                        actualVehiclesNames = ""
                        for vehicleName in peopleInfo.getVehicles():
                            actualVehiclesNames += vehicleName + ", "
                        vehicleName = raw_input("Enter the name of the vehicle to remove.\n"
                                                "Actual vehicles names : {}\n".format(actualVehiclesNames))
                        vehicleData = self._dataBaseManager.getVehiclesInfo([vehicleName], False)
                        if len(vehicleData) != 0:
                            try:
                                peopleInfo.removeVehicle(vehicleName)
                            except ValueError:
                                print "Vehicle is not hold by this people. Not removed.\n"
                            else:
                                _updateListData(TablePeople.COLUMN_VEHICLES, 0, vehicleData[0].getId())
                        else:
                            print "Vehicle does not exist. Not removed.\n"
                elif y == '12':
                    self._dataBaseManager.updatePeopleInfo(peopleInfo.getId(), newData)
                    toContinue = True
                elif y == '13':
                    print "people => \n", peopleInfo.getStr(), "\n"
                elif y == '14':
                    toContinue = False

    def _deletingPeopleMode(self):
        """Method letting to delete a row from the people table.
        The user chose the row he wants to remove and it is removed from the table.
        The user can ask to remove several row in the same time.

        :return: None.
        """
        manual = "Enter the names of people you want to delete.\n" \
                 "Finish the list by an empty names.\n" \
                 "To come back to previous mode, enter a empty list.\n\n"

        toContinue = True
        listNames = []
        while toContinue:
            x = raw_input(manual)
            if x == '':
                if listNames:
                    for n in listNames:
                        peopleInfoList = self._dataBaseManager.getPeopleInfo(listNames)
                        if len(peopleInfoList) == 0:
                            print 'None info found for name {}'.format(n)
                        elif len(peopleInfoList) == 1:
                            self._dataBaseManager.deletePeople(peopleInfoList[0].getId())
                        else:
                            try:
                                pNumber = self._choicePeopleFromList(n, peopleInfoList)
                            except ValueError:
                                print 'Wrong number entered. Request canceled'
                            else:
                                if pNumber != -1:
                                    if pNumber > len(peopleInfoList):
                                        print 'Wrong number entered. Request canceled'
                                    else:
                                        self._dataBaseManager.deletePeople(peopleInfoList[pNumber].getId())
                                else:
                                    for p in peopleInfoList:
                                        self._dataBaseManager.deletePeople(p.getId())
                else:
                    toContinue = False
                listNames = []
            else:
                if "'" in x or '"' in x:
                    print "{} or {} characters can not be in name people".format("'", '"')
                else:
                    listNames.append(x)

    def _choicePeopleFromList(self, name, peopleList):
        """Method letting to choice a row from many.

        :return: return the relative index of the row chosen (in the sub list of possible rox) - int.
        """
        print 'Several people have this name {}\n'.format(name)
        for i, p in enumerate(peopleList):
            print 'people number => {}'.format(str(i))
            print p
            print "\n"
        print 'Enter the number of the people you really want to remove'
        print 'If you want to remove all these peoples, enter -1'
        print 'all others characters will canceled the request'
        y = raw_input()
        return int(y)

    def _closeApp(self):
        """Close the application

        :return: None.
        """
        self._dataBaseManager.closeConnection()
