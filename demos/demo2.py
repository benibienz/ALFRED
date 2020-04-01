""" More complex input/action demo """

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.exceptions import NotFittedError
import warnings
warnings.filterwarnings('ignore')  # sklearn is annoying with warnings


def gen_input():
    """ Generate input vector """
    x = np.random.randint(1, 20, 4)
    x[np.random.randint(0, 4)] = 0
    return x


if __name__ == '__main__':

    # init some stuff
    clf = GaussianNB()  # we are using a Gaussian Naive Bayes classifier for now
    N = 100  # number of observations
    observations, actions = [], []  # init observation and action arrays

    for i in range(N):
        x = gen_input()
        try:
            # predict action with and associated probability
            pred = clf.predict(np.array(x).reshape(1, -1))[0]
            probs = clf.predict_proba(np.array(x).reshape(1, -1))[0]
            # print(probs)
            try:
                prob = probs[pred - 1]
            except IndexError:
                prob = 0.25
        except NotFittedError:
            pred, prob = None, 0.25  # first round we have no predictions

        print(f'Input:  {x}             Predicted action: {pred}  ({100 * prob:.0f}% probability)')
        y = int(input('Action: '))

        # append new input and action
        observations.append(x)
        actions.append(y)
        clf.fit(observations, actions)