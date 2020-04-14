import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
from sklearn.exceptions import NotFittedError
import warnings

plt.switch_backend('Agg')  # stops weird shit from happening
warnings.filterwarnings('ignore')  # sklearn is annoying with warnings

# Space state parameters
ID_LIST = ['US', 'RUS', 'DEBRIS']
STATE_KEYS = ['ID', 'Velocity deviation', 'X', 'Y', 'Z', 'Missed pass count']
STATE_TYPES = ['enum', 'float', 'float', 'float', 'float', 'int']
ACTION_NAMES = ['Do Nothing', 'Investigate']


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


class Recommender:
    def __init__(self, state_type='space', clf_type='tree', max_n=1000):

        self.state_type = state_type
        if state_type == 'space':
            self.state_generator = gen_space_state
            self.action_size = 2
            self.clf_type = clf_type
        else:
            self.state_generator = gen_state
            self.action_size = 4
            self.clf_type = 'nb'  # no trees for this state type

        self.clf = DecisionTreeClassifier() if clf_type == 'tree' else GaussianNB()
        self.max_N = max_n  # max number of steps
        self.N = 0  # current step

        self.states, self.actions, self.pred_history, self.prob_history = [], [], [], []

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

    def train(self):
        self.clf.fit(self.states, self.actions)
        self.save_tree_graph()

    def reset(self):
        self.__init__(state_type=self.state_type, max_n=self.max_N, clf_type=self.clf_type)

    def save_tree_graph(self):
        export_graphviz(self.clf, out_file='static/images/tree_viz', class_names=ACTION_NAMES, feature_names=STATE_KEYS,
                        precision=1, rounded=True, filled=True, impurity=False, label='none')
        plot_tree(self.clf, class_names=ACTION_NAMES, feature_names=STATE_KEYS, precision=1,
                  rounded=True, filled=True, impurity=False, label='none')
        plt.savefig('static/images/tree_graph')


if __name__ == '__main__':

    model = Recommender(max_n=10, state_type='simple')
    for _ in range(model.max_N):
        s, pred, probs = model.display_next_state()
        print(f'Input:  {s}           Predicted action: {pred}  ({[100 * p for p in probs]}% probability)')
        a = int(input('Action: '))
        model.states.append(s)
        model.actions.append(a)
        model.train()

    model.save_tree_graph()
