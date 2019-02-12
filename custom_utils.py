import pickle

def export(docs, filename):
    '''
    To export list to pickle.

    Accept 2 parameters : the list to be exported & the filename of the exported file.
    Define the destination folder of the exported file in the filename.
    '''

    save_path = "D:\Kuliah\TA\data"

    with open(save_path + "\\" + filename, 'wb') as output:
        pickle.dump(docs, output)