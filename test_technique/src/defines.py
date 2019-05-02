# !/usr/bin/env python
# -*- coding: utf-8 -*-


class TablePeople(object):
    ID = "people"

    COLUMN_ID = "id"
    COLUMN_URL = "url"
    COLUMN_NAME = "name"
    COLUMN_HEIGHT = "height"
    COLUMN_MASS = "mass"
    COLUMN_HAIR_COLOR = "hair_color"
    COLUMN_SKIN_COLOR = "skin_color"
    COLUMN_EYE_COLOR = "eye_color"
    COLUMN_BIRTH_YEAR = "birth_year"
    COLUMN_GENDER = "gender"
    COLUMN_HOME_WORLD = "homeworld"
    COLUMN_DATE_CREATED = "created"
    COLUMN_DATA_EDITED = "edited"
    COLUMN_STAR_SHIPS = "starships"
    COLUMN_VEHICLES = "vehicles"


class TablePeopleStarShips(object):
    ID = "people_starships"

    COLUMN_PEOPLE = "people"
    COLUMN_STAR_SHIPS = "starships"


class TablePeopleVehicles(object):
    ID = "people_vehicles"

    COLUMN_PEOPLE = "people"
    COLUMN_VEHICLES = "vehicles"


class TableStarShips(object):
    ID = "starships"

    COLUMN_NAME = "name"
    COLUMN_MODEL = "model"
    COLUMN_MANUFACTURER = "manufacturer"
    COLUMN_COST = "cost_in_credits"
    COLUMN_LENGTH = "length"
    COLUMN_MAX_SPEED = "max_atmosphering_speed"
    COLUMN_CREW = "crew"
    COLUMN_PASSENGERS = "passengers"
    COLUMN_CARGO_CAPACITY = "cargo_capacity"
    COLUMN_CONSUMABLES = "consumables"
    COLUMN_HYPERDRIVE_RATING = "hyperdrive_rating"
    COLUMN_MGLT = "MGLT"
    COLUMN_STAR_SHIP_CLASS = "starship_class"
    COLUMN_PILOTS = "pilots"
    COLUMN_FILMS = "films"
    COLUMN_DATE_CREATED = "created"
    COLUMN_DATE_EDITED = "edited"
    COLUMN_URL = "url"
    COLUMN_ID = "id"


class TableVehicles(object):
    ID = "vehicles"

    COLUMN_NAME = "name"
    COLUMN_MODEL = "model"
    COLUMN_MANUFACTURER = "manufacturer"
    COLUMN_COST = "cost_in_credits"
    COLUMN_LENGTH = "length"
    COLUMN_MAX_SPEED = "max_atmosphering_speed"
    COLUMN_CREW = "crew"
    COLUMN_PASSENGERS = "passengers"
    COLUMN_CARGO_CAPACITY = "cargo_capacity"
    COLUMN_CONSUMABLES = "consumables"
    COLUMN_VEHICLE_CLASS = "vehicle_class"
    COLUMN_PILOTS = "pilots"
    COLUMN_FILMS = "films"
    COLUMN_DATE_CREATED = "created"
    COLUMN_DATE_EDITED = "edited"
    COLUMN_URL = "url"
    COLUMN_ID = "id"


class TablePlanets(object):
    ID = "planets"
    COLUMN_NAME = "name"
    COLUMN_ROTATION_PERIOD = "rotation_period"
    COLUMN_ORBITAL_PERIOD = "orbital_period"
    COLUMN_DIAMETER = "diameter"
    COLUMN_CLIMATE = "climate"
    COLUMN_GRAVITY = "gravity"
    COLUMN_TERRAIN = "terrain"
    COLUMN_SURFACE_WATER = "surface_water"
    COLUMN_POPULATION = "population"
    COLUMN_RESIDENTS = "residents"
    COLUMN_FILMS = "films"
    COLUMN_CREATED = "created"
    COLUMN_EDITED = "edited"
    COLUMN_URL = "url"
    COLUMN_ID = "id"


class TableSpecies(object):
    ID = "species"

    COLUMN_NAME = "name"
    COLUMN_CLASSIFICATION = "classification"
    COLUMN_DESIGNATION = "designation"
    COLUMN_AVERAGE_HEIGHT = "average_height"
    COLUMN_SKIN_COORS = "skin_colors"
    COLUMN_HAIR_COLORS = "hair_colors"
    COLUMN_EYE_COLORS = "eye_colors"
    COLUMN_AVERAGE_LIFE_SPAN = "average_lifespan"
    COLUMN_HOME_WORLD = "homeworld"
    COLUMN_LANGUAGE = "language"
    COLUMN_PEOPLE = "people"
    COLUMN_FILMS = "films"
    COLUMN_CREATED = "created"
    COLUMN_EDITED = "edited"
    COLUMN_URL = "url"
    COLUMN_ID = "id"


class TableFilms(object):
    ID = "films"

    COLUMN_TITLE = "title"
    COLUMN_EPISODE_ID = "episode_id"
    COLUMN_OPENING_CRAWL = "opening_crawl"
    COLUMN_DIRECTOR = "director"
    COLUMN_PRODUCER = "producer"
    COLUMN_RELEASE_DATE = "release_date"
    COLUMN_CHARACTERS = "characters"
    COLUMN_PLANETS = "planets"
    COLUMN_STAR_SHIPS = "starships"
    COLUMN_VEHICULES = "vehicles"
    COLUMN_SPECIES = "species"
    COLUMN_DATE_CREATED = "created"
    COLUMN_DATE_EDITED = "edited"
    COLUMN_URL = "url"
    COLUMN_ID = "id"


class TableFilmsPlanets(object):
    ID = "films_planets"

    COLUMN_FILM = "films"
    COLUMN_PLANET = "planets"


class TablePeopleSpecies(object):
    ID = "people_species"

    COLUMN_PEOPLE = "people"
    COLUMN_SPECIES = "species"


class TableFilmsSpecies(object):
    ID = "films_species"

    COLUMN_FILMS = "films"
    COLUMN_SPECIES = "species"


class TableFilmsPeoples(object):
    ID = "films_people"

    COLUMN_PEOPLE = "people"
    COLUMN_FILMS = "films"


class TableFilmsStarShips(object):
    ID = "films_starships"

    COLUMN_FILMS = "films"
    COLUMN_STAR_SHIPS = "starships"


class TableFilmsVehicles(object):
    ID = "films_vehicles"

    COLUMN_VEHICLES = "vehicles"
    COLUMN_FILMS = "films"
