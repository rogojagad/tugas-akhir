import json
from custom_utils import *
from pprint import pprint

with open("dataset/test-dataset.json") as f:
    dataset = json.load(f)

result = list()

for idx, data in enumerate(dataset):
    sentiment_aspect_pair = dict()
    temp = dict()
    sentiment_aspect_pair["id"] = idx

    for sentiment, aspect in zip(data["polarity"], data["target"]):
        if aspect != "NULL":

            temp[aspect] = sentiment

    sentiment_aspect_pair["data"] = temp

    result.append(sentiment_aspect_pair)

export(result, "/test/aspect_sentiment_truth.pickle")
