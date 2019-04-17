import pickle
import json
from pprint import pprint

with open("D://Kuliah/TA/data/test/sentiment_analyze_result.pickle", "rb") as inp:
    results = pickle.load(inp)

with open("D://Kuliah/TA/data/test/aspect_sentiment_truth.pickle", "rb") as inp:
    truths = pickle.load(inp)

with open("dataset/test-dataset.json") as f:
    dataset = json.load(f)

error_counter = 0
missing = 0
aspect_count = 0

for truth, result, data in zip(truths, results, dataset):
    for aspect, sentiment in truth["data"].items():
        aspect_count += 1
        try:
            if result["data"][aspect] != sentiment:
                print(data["sentence"])
                print(result["id"])
                print(aspect)
                print("Truth")
                print(sentiment)
                print("Result")
                print(result["data"][aspect])
                print()
                error_counter += 1
        except KeyError:
            missing += 1
            continue

print("Aspect count : {}".format(aspect_count))
print("Accuracy : {}".format((aspect_count - error_counter) / aspect_count))
print("Error : {}".format(error_counter))
print("Missing : {}".format(missing))
