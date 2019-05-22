import pandas as pd
import math
import json
from pprint import pprint
from custom_utils import *

df = pd.read_excel("D:\Kuliah/TA/data/general-inquirer/inquirerbasic.xls")

lexicon = dict()

for i in df.index:
    word = df["Entry"][i].lower().split("#")[0]
    positive = df["Positiv"][i]
    negative = df["Negativ"][i]
    polarity = ""

    if isinstance(positive, str):  # Value is "Positiv"
        polarity = "positive"
    elif isinstance(negative, str):  # Value is "Negativ"
        polarity = "negative"
    else:
        polarity = "neutral"

    if word not in lexicon:
        lexicon[word] = polarity

with open("D:\Kuliah\TA\data\general-inquirer\lexicon.json", "w") as fp:
    json.dump(lexicon, fp)
