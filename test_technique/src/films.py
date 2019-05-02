# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Film(object):
    """
    Class representing a film.
    """
    def __init__(self, _id, title, episodeId="", openingCrawl="", director="", producer="", releaseDate="",
                 peoplesList=None, planetsList=None, starShipsList=None, vehiclesList=None, speciesList=None):
        self._id = _id
        self._title = title
        self._episodeId = episodeId
        self._openingCrawl = openingCrawl
        self._director = director
        self._producer = producer
        self._releaseDate = releaseDate
        self._peoplesList = peoplesList if peoplesList is not None else []
        self._planetsList = planetsList if planetsList is not None else []
        self._starShipsList = starShipsList if starShipsList is not None else []
        self._vehiclesList = vehiclesList if vehiclesList is not None else []
        self._speciesList = speciesList if speciesList is not None else []

    def getId(self):
        return self._id

    def getTitle(self):
        return self._title

    def __str__(self):
        info = "Title : {}\nEpisode id : {}\nDirector : {}\nProducer : {}\nRelease date : {}\n Opening crawl : {}\n" \
               "Peoples that appears in this film : {}\nPlanets that appear in this film : {}\n" \
               "Star ships that appear in this film : {}\nVehicles that appear in this film : {}\n" \
               "Species that appear in this film : {}".\
            format(self._title, self._episodeId, self._director, self._producer, self._releaseDate, self._openingCrawl,
                   self._peoplesList, self._planetsList, self._starShipsList, self._vehiclesList, self._speciesList)

        return info

    def getStr(self):
        return self.__str__()
