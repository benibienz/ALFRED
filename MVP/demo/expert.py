import numpy as np
import numpy.random as rand
from sklearn.naive_bayes import GaussianNB
from sklearn.exceptions import NotFittedError
import warnings

warnings.filterwarnings('ignore')  # sklearn is annoying with warnings

# Space state parameters
ID_LIST = ['US', 'RUS', 'DEBRIS']
STATE_KEYS = ['ID', 'Velocity deviation', 'X', 'Y', 'Z', 'Missed pass count']
STATE_TYPES = ['enum', 'float', 'float', 'float', 'float', 'int']


def gen_state():
    """ Generate random state """
    s = rand.randint(1, 9, 4)
    s[rand.randint(0, 4)] = 0
    return s


def transform_space_state(state):
    if isinstance(state, dict):
        arr = [ID_LIST.index(state['ID'])] + [state[k] for k in STATE_KEYS[1:]]
        return np.array(arr)
    else:
        s_dict = {'ID': ID_LIST[int(state[0])]}
        for i, k in enumerate(STATE_KEYS[1:]):
            s_dict[k] = state[i + 1]
        return s_dict


def gen_space_state():
    """ Generate random space state """
    s_dict = {
        'ID': rand.choice(ID_LIST),
        'Velocity deviation': abs(rand.normal()),
        'X': rand.uniform(0, 100),
        'Y': rand.uniform(0, 10),
        'Z': rand.uniform(0, 100),
        'Missed pass count': rand.choice([0, 0, 0, 0, 1, 1, 2])
    }
    s = transform_space_state(s_dict)
    return s


class Expert:
    def __init__(self, state_type='space', max_n=1000):
        self.clf = GaussianNB()  # we are using a Gaussian Naive Bayes classifier for now
        self.max_N = max_n  # max number of steps
        self.N = 0  # current step

        if state_type == 'space':
            self.state_generator = gen_space_state
            self.action_size = 2
        else:
            self.state_generator = gen_state
            self.action_size = 4

    def display_next_state(self):
        if self.N == self.max_N:
            raise StopIteration('Max N reached')
        state = self.state_generator()
        try:
            # predict action with an associated probability
            pred_action = self.clf.predict(np.array(state).reshape(1, -1))[0]
            probs = self.clf.predict_proba(np.array(state).reshape(1, -1))[0]
            print(probs)
            if len(probs) < self.action_size:
                probs = [1 / self.action_size] * self.action_size

        except NotFittedError:
            pred_action, probs = 0, [1 / self.action_size] * self.action_size  # first round we have no predictions

        self.N += 1
        return state, pred_action, probs

    def train(self, states, actions):
        self.clf.fit(states, actions)


if __name__ == '__main__':

    model = Expert()
    states, actions = [], []
    for _ in range(model.max_N):
        s, pred, probs = model.display_next_state()
        print(f'Input:  {transform_space_state(s)}           Predicted action: {pred}  ({[100 * p for p in probs]}% probability)')
        a = int(input('Action: '))
        states.append(s)
        actions.append(a)
        model.train(states, actions)