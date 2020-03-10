""" Very simple binary input/action demo """

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.exceptions import NotFittedError
import warnings
warnings.filterwarnings('ignore')  # sklearn is annoying with warnings


def gen_input():
    """ Generate input vector """
    return np.random.randint(0, 2)


if __name__ == '__main__':

    # init some stuff
    clf = GaussianNB()  # we are using a Gaussian Naive Bayes classifier for now
    N = 100  # number of observatuibs
    observations, actions = [], []  # init observation and action arrays

    for i in range(N):
        x = gen_input()
        try:
            # predict action with and associated probability
            pred = clf.predict(np.array(x).reshape(1, -1))[0]
            probs = clf.predict_proba(np.array(x).reshape(1, -1))[0]
            prob = 0.5 if len(probs) == 1 else probs[pred]
        except NotFittedError:
            pred, prob = None, 0.5  # first round we have no predictions

        print(f'Input:  {x}             Predicted action: {pred}  ({100 * prob:.0f}% probability)')
        y = int(input('Action: '))

        # append new input and action
        observations.append([x])
        actions.append(y)
        clf.fit(observations, actions)
