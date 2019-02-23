import pickle
# from nltk.tokenize import RegexpTokenizer
from custom_utils import export
from pprint import pprint
from tqdm import tqdm

# with open("D:\Kuliah\TA\data\\test\\labelled_words.pickle", "rb") as inp:
#     words = pickle.load(inp)

with open("D:\Kuliah\TA\data\\test\\prediction_result.pickle", "rb") as inp:
    results = pickle.load(inp)

pprint(results)

# tokenizer = RegexpTokenizer(r'\w+')

# needed_relation = ['amod', 'nsubj', 'dependent']
# tokenized = tokenizer.tokenize('Ive asked a cart attendant for a lotus leaf wrapped rice and she replied back rice and just walked\n                    away.\n                ')

# print("Relation as governor :")
# rel = {}
# for token in tokenized:
#     for data in results:
#         if data[0][0] == token and data[1] in needed_relation:
#             if token in rel:
#                 if data[1] not in rel[token].split(';'):
#                     rel[token] += ';' + data[1]
#             else:
#                 rel[token] = data[1]

# pprint(rel)

# print("Relation as dependent :")
# rel = {}
# for token in tokenized:
#     for data in results:
#         if data[2][0] == token:
#             if token in rel:
#                 if data[1] not in rel[token].split(';'):
#                     rel[token] += ';' + data[1]
#             else:
#                 rel[token] = data[1]

# pprint(rel)
