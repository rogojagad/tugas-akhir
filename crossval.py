import pickle
import scipy.stats
import sklearn_crfsuite
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV
from sklearn_crfsuite import metrics

data_dir = "D:\Kuliah\TA\data"

with open(data_dir + "\\train\\features.pickle", "rb") as inp:
    X_train = pickle.load(inp)

with open(data_dir + "\\train\\labels.pickle", "rb") as inp:
    y_train = pickle.load(inp)

with open(data_dir + "\\test\\features.pickle", "rb") as inp:
    X_test = pickle.load(inp)

with open(data_dir + "\\test\\labels.pickle", "rb") as inp:
    y_test = pickle.load(inp)

crf = sklearn_crfsuite.CRF(algorithm="lbfgs", all_possible_transitions=True)

params_space = {"c1": scipy.stats.expon(scale=0.5), "c2": scipy.stats.expon(scale=0.05)}

f1_scorer = make_scorer(metrics.flat_f1_score, average="weighted")

rs = RandomizedSearchCV(
    crf, params_space, verbose=1, n_jobs=-1, n_iter=50, scoring=f1_scorer
)

rs.fit(X_train, y_train)

print("Best params : ", rs.best_params_)
print("Best CV score : ", rs.best_score_)
print("model size: {:0.2f}M".format(rs.best_estimator_.size_ / 1000000))

