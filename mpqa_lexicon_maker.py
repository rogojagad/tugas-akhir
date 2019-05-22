import json
from pprint import pprint
from custom_utils import export

with open("D:/Kuliah/TA/data/mpqa_lexicon/lexicon.tff", "r") as f:
    file_content = f.readlines()

list_of_datum = []
restructured_data = {}

for datum in file_content:
    splitted = datum.strip("\n").split(" ")
    list_of_datum.append(splitted)

# pprint(list_of_datum[0][5])

i = 0

for datum in list_of_datum:
    temp = {}

    subjectivity = datum[0].split("=")[1]
    polarity = datum[5].split("=")[1]
    pos_tag = datum[3].split("=")[1]
    word = datum[2].split("=")[1]

    temp["subjectivity"] = subjectivity
    temp["polarity"] = polarity
    temp["pos_tag"] = pos_tag

    restructured_data[word] = temp

# pprint(restructured_data)
with open("D:\Kuliah\TA\data\mpqa_lexicon\lexicon.json", "w") as fp:
    json.dump(restructured_data, fp)

# export(data.split("\n"), "\\general-inquirer\\positive-words.pickle")
