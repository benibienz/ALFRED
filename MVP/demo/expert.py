import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.exceptions import NotFittedError
import warnings

warnings.filterwarnings('ignore')  # sklearn is annoying with warnings


def gen_state():
    """ Generate random state """
    x = np.random.randint(1, 9, 4)
    x[np.random.randint(0, 4)] = 0
    return x


class Expert:
    def __init__(self, max_n=100):
        self.clf = GaussianNB()  # we are using a Gaussian Naive Bayes classifier for now
        self.max_N = max_n  # max number of steps
        self.N = 0  # current step

    def display_next_state(self):
        if self.N == self.max_N:
            raise StopIteration('Max N reached')
        state = gen_state()
        try:
            # predict action with an associated probability
            pred_action = self.clf.predict(np.array(state).reshape(1, -1))[0]
            probs = self.clf.predict_proba(np.array(state).reshape(1, -1))[0]
            print(probs)
            if len(probs) < 4:
                probs = [0.25] * 4

        except NotFittedError:
            pred_action, probs = 0, [0.25] * 4  # first round we have no predictions

        self.N += 1
        return state, pred_action, probs

    def train(self, states, actions):
        self.clf.fit(states, actions)


if __name__ == '__main__':
    model = Expert()
    states, actions = [], []
    for _ in range(model.max_N):
        s, _, _ = model.display_next_state()
        a = int(input('Action: '))
        states.append(s)
        actions.append(a)
        model.train(states, actions)