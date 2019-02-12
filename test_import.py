import pickle
from pprint import pprint

with open("D:\Kuliah\TA\data\\test\\features.pickle", "rb") as inp:
    lst = pickle.load(inp)

pprint(lst[0])