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