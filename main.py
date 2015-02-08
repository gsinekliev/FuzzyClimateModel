import input as inp
import os


def main():
    #data = inp.InputDataUtilities.getNumpyArrayListFromFile( os.getcwd() + '\\Data\\data_norm_2012_2013.npy' )
    #data = inp.InputDataUtilities.getNumpyArrayListFromFile( os.getcwd() + '\\Data\\data_temp_2012_2013.npy' )
    data = inp.InputDataUtilities.getNumpyArrayListFromFile( os.getcwd() + '\\Data\\data_january_2012_2013.npy' )

    training_data =[ t.flatten() for t in data ]

    named_training_data = zip(inp.perc_cities, training_data)

    print named_training_data

if __name__ == '__main__':
    main()
