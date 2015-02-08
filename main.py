import input as inp
import os


def main():
    # data = inp.InputDataUtilities.getNumpyArrayListFromFile( os.getcwd() + '\\Data\\data_norm_2012_2013.npy' )
    data = inp.InputDataUtilities.getNumpyArrayListFromFile( os.getcwd() + '\\Data\\data_temp_2012_2013.npy' )

    print data;


if __name__ == '__main__':
    main()
