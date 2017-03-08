#!/usr/bin/env python
import array

from collections import namedtuple

# KDTree for storing 2 dimensional location in binary tree
from scipy.spatial import cKDTree as KDTree

TAB_SEP = '\t'

GEONAMES_CITIES_FILE = 'cities1000.txt'

CityInfo = namedtuple('CityInfo', 'name asciiname altnames latitude longitude '
                                  'feature_code country_code country')


class GeoNames:

    def __init__(self):
        self.locations = []
        self.city_info = []
        self.kdtree = None
        self.kdtree_per_country = {}
        self.geoname_lat_lng_mapping = {}

        # Setup intial mapping and location dicts
        self.initial_setup()

    def readfile(self):
        """Returns lines in 'cities1000.txt' as generator"""
        try:
            with open(GEONAMES_CITIES_FILE) as fileobj:
                for line in fileobj:
                    yield line
        except IOError:
            print('Invalid filename')

    def initial_setup(self):
        """Parse 'cities1000.txt' and create dictionary for holding cities info
        and mapping between latitude, longitude and city info"""
        if not self.locations or not self.geoname_lines:
            for line in self.readfile():
                items = line.split(TAB_SEP)

                # Create CityInfo object and append to list
                self.city_info.append(CityInfo(items[1], items[2], items[3],
                                               float(items[4]), float(items[5]),
                                               items[7], items[8], 'None'))

                latitude, longitude = float(items[4]), float(items[5])
                self.geoname_lat_lng_mapping[(latitude, longitude)] = items
                self.locations.append([latitude, longitude])

        # Insert all locations into KDTree
        self.kdtree = KDTree(self.locations)

    def find_locations(self, country):
        """Find all cities(latitude, longitude) for given country"""
        locations = []

        for cityinfo in self.city_info:
            if country == cityinfo.country_code:
                locations.append((cityinfo.latitude, cityinfo.longitude))

        # Need to return empty array for checking False result
        return locations if locations else array.array('l', [])

    def query(self, location, k, country=None):
        """Query KDTree for k nearest cities"""
        if not country:
            return self.kdtree.query(location, k=k)
        else:
            if not self.kdtree_per_country.get(country):
                locations = self.find_locations(country=country)

                if len(locations) == 0:
                    return (None, locations)

                self.kdtree_per_country[country] = KDTree(locations)

            return self.kdtree_per_country[country].query(location, k=k)

# Global object reference
geoname = None


def geonames():
    """Hacky way of getting refrence to GeoNames object"""
    global geoname

    if not geoname:
        geoname = GeoNames()

    return geoname


def is_valid_city(keyword, cityinfo):
    """Returns True is city name is valid and found in either
    name, asciiname or altnames"""
    return keyword.lower() in cityinfo.name.lower() or \
        keyword.lower() in cityinfo.asciiname.lower() or \
        keyword.lower() in cityinfo.altnames.lower()


def is_city(cityinfo):
    """Returns True if city is actual city and not district"""
    for feature_code in ['PPL', 'PPLC', 'PPLA']:
        if feature_code == cityinfo.feature_code:
            return True


def find_cities(keyword):
    """Handler for '/v1.0/cities/{name}' endpoint.
    Returns all cities which match keyword"""
    result = []

    for cityinfo in geonames().city_info:
        if is_valid_city(keyword, cityinfo) and is_city(cityinfo):
            result.append(dict(city=cityinfo.name,
                               country_code=cityinfo.country_code))

    return result if result else 'Not found'


def find_city(city):
    """Finds latitude and longitude of city"""
    for cityinfo in geonames().city_info:
        if is_valid_city(city, cityinfo):
            return (cityinfo.latitude, cityinfo.longitude)

    return (None, None)


def find_k_nearest_cities(city, k, country=None):
    """Handler for '/v1.0/nearest_cities/' endpoint.
    Finds k nearest cities using KDTree"""
    result = []

    (latitude, longitude) = find_city(city)

    if not latitude or not longitude:
        return 'City not found!'

    # Insert latitude & longitude of all cities in geonames db to KDTree
    _, indices = geonames().query((latitude, longitude),
                                  k=k,
                                  country=country)

    if len(indices) == 0:
        return 'Invalid parameters. Please check your parameters'

    # For each index return by query find latitude, longitude
    # which maps to the city info.
    for index in indices:
        if not country:
            latitude, longitude = geonames().kdtree.data[index]
        else:
            latitude, longitude = \
                geonames().kdtree_per_country[country].data[index]

        city = geonames().geoname_lat_lng_mapping[(latitude, longitude)]

        result.append(dict(city=city[1], country_code=city[8]))
        print(geonames().geoname_lat_lng_mapping[(latitude, longitude)])

    return result
