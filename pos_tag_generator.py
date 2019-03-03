import nltk
import json
import pickle
from tqdm import tqdm
from pprint import pprint
from nltk.tokenize import RegexpTokenizer
from custom_utils import export

with open('dataset/train-dataset.json') as f:
    dataset = json.load(f)

tagged = []

for i in tqdm(range(len(dataset))):
    tokenizer = RegexpTokenizer(r'\w+')

    tokenized = tokenizer.tokenize(dataset[i]['sentence'])

    tagged.append(nltk.pos_tag(tokenized))

save_path = "D:\Kuliah\TA\data"

with open(save_path + "\\" + "train\word_with_pos_tag.pickle", 'wb') as output:
    pickle.dump(tagged, output)