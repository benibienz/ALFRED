""" Scratch file for testing stuff - ignore this """

import numpy as np
from sklearn.naive_bayes import GaussianNB

num_inputs = 2
num_actions = 2

# Generate input
X = []
N = 2

for _ in range(N):
    x = [0] * num_inputs
    x[np.random.randint(0, num_inputs)] = 1
    X.append(x)

X = np.array(X)
# print(X)

# assign action labels
Y = []

for x in X:
    r = np.random.randint(0, 10)
    if r > 3:
        action = np.random.randint(0, 2)
    elif x[0] == 1:
        action = 1
    else:
        action = 0
    Y.append(action)

Y = np.array(Y)
# print(Y)


clf = GaussianNB()
clf.fit(X, Y)

clf.score(X, Y)

# print(clf.predict(X))
print(clf.predict_proba([[0, 1], [1, 0]]))


