import json
from custom_utils import *
from pprint import pprint

with open("dataset/test-dataset.json") as f:
    dataset = json.load(f)

result = dict()

for idx, data in enumerate(dataset):
    sentiment_aspect_pair = list()

    for sentiment, aspect in zip(data["polarity"], data["target"]):
        if aspect != "NULL":
            sentiment_aspect_pair.append((sentiment, aspect))

    result[idx] = sentiment_aspect_pair

export(result, "/test/aspect_sentiment_truth.pickle")
