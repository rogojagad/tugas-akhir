import json
from custom_utils import *
from pprint import pprint

with open("dataset/test-dataset.json") as f:
    data = json.load(f)

temp_frequent_at = {}
final_frequent_at = {}

for datum in data:
    for target in datum["target"]:
        if target != "NULL":
            if target not in temp_frequent_at:
                temp_frequent_at[target] = 1
            else:
                temp_frequent_at[target] += 1

for name, count in temp_frequent_at.items():
    if count > 5:
        final_frequent_at[name] = count

pprint(final_frequent_at)

export(final_frequent_at, "train\\frequent_term.pickle")
