import numpy as np
import os

class InputDataUtilities(object):
    """Utilities for reading/writing to files"""
    @staticmethod
    def getNumpyArrayListFromFile( arrays_path ):
        """ Returns a list of numpy arrays - the training set"""
        arrays_list = []
        with open(arrays_path, 'rb') as fobj:
            while 1:
                try:
                    t = np.load(fobj)
                    arrays_list.append(t)
                except Exception as e:
                    print e
                    break
        return arrays_list

    @staticmethod
    def saveNumpyArrayListToFile( array_list, fileName ):
        with open( os.getcwd() + '\\Data\\' + fileName, "ab" ) as fObj:
            for row in array_list:
                np.save( fObj, row )


""" There is percepitation info for these cities after July 2012"""
perc_cities = ['Aalborg', 'Alicante', 'Amsterdam', 'Ankara', 'Antalya', 'Arad', 'Atlanta', 'Baltimore',
               'Barcelona', 'Basel', 'Beijing', 'Beirut', 'Belfast', 'Belgrade', 'Bergen', 'Berlin', 'Bogota', 'Boston',
               'Brasilia', 'Bremen', 'Brisbane', 'Bristol', 'Brno', 'Brussels', 'Bucharest', 'Burgas', 'Cairo', 'Charlotte',
               'Chicago', 'Copenhagen', 'Corfu', 'Craiova', 'Dalian', 'Dallas', 'Debrecen', 'Denver',
               'Diyarbakir', 'Dongguan', 'Dubai', 'Dublin', 'Dusseldorf', 'Eindhoven', 'Fort Lauderdale', 'Frankfurt',
               'Geneva', 'Graz', 'Guangzhou', 'Hahn', 'Hamburg', 'Hangzhou', 'Hannover', 'Hanover', 'Helsinki',
               'Ho Chi Minh City', 'Hong Kong', 'Honolulu', 'Houston', 'Iasi', 'Incheon', 'Istanbul', 'Karachi', 'Kiev',
               'Kinshasa', 'Klagenfurt', 'Kosice', 'Krakow', 'Kristiansand', 'Kuala Lumpur', 'Kunming', 'Lagos', 'Las Vegas',
               'Leeds', 'Liege', 'London', 'Los Angeles', 'Luqa', 'Luxembourg', 'Madrid', 'Malaga', 'Malmo', 'Melbourne',
               'Mexico City', 'Miami', 'Milan', 'Minneapolis', 'Mulhouse', 'Mumbai', 'Munich', 'Natal', 'New York',
               'Newcastle', 'Nice', 'Orlando', 'Oslo', 'Palma De Mallorca', 'Palma de Mallorca', 'Philadelphia', 'Phoenix',
               'Pisa', 'Prague', 'Riga', 'Riyadh', 'Salt Lake City', 'Salvador', 'Salzburg', 'San Diego', 'San Francisco',
               'Sao Paulo', 'Seattle', 'Shenzhen', 'Singapore', 'Skopje', 'Sofia', 'Split', 'Stuttgart', 'Sydney',
               'Tampa', 'Tehran', 'Thessaloniki', 'Toronto', 'Toulouse', 'Trondheim', 'Ufa', 'Valencia', 'Vancouver', 'Varna',
               'Verona', 'Vienna', 'Warsaw', 'Washington', 'Wroclaw', 'Xiamen', 'Yekaterinburg', 'Zaragoza', 'Zurich']

