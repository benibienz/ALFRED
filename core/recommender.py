import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
from sklearn.exceptions import NotFittedError
import warnings

plt.switch_backend('Agg')  # stop matplotlib ruining everything
warnings.filterwarnings('ignore')  # sklearn is annoying with warnings

# Space state parameters
ID_LIST = ['US', 'RUS', 'EU', 'UNKNOWN']
OBJECT_TYPE_LIST = ['DEBRIS', 'SATELLITE', 'UNKNOWN']
STATE_KEYS = ['ID', 'Object type', 'Velocity deviation', 'Latitude', 'Longitude',
              'Missed pass count']
STATE_KEYS += ['Year first seen']
ACTION_KEYS = ['No Action', 'Track Object', 'Alert']


class StateVar:
    def __init__(self, name, val, kind='float', val_list=None):
        self.name = name
        self.val = val
        self.kind = kind
        self.val_list = val_list

    def get_val(self):
        if self.kind == 'enum':
            return self.val_list.index(self.val)
        else:
            return self.val

    def get_val_str(self):
        if self.kind == 'enum':
            return self.val
        elif self.kind == 'int':
            return f'{self.val:.0f}'
        else:
            return f'{self.val:.1f}'


def gen_state():
    """ Generate random state """
    s = rand.randint(1, 9, 4)
    s[rand.randint(0, 4)] = 0
    return s


def state2vec(state):
    return np.array([v.get_val() for v in state])


def gen_space_state():
    """ Generate random space state """
    s_id = StateVar('ID', rand.choice(ID_LIST), kind='enum', val_list=ID_LIST)
    s_type_choice = 'UNKNOWN' if s_id.get_val_str() == 'UNKNOWN' else rand.choice(OBJECT_TYPE_LIST[:-1])
    s_type = StateVar('Object type', s_type_choice, kind='enum', val_list=OBJECT_TYPE_LIST)
    s = [
        s_id,
        s_type,
        StateVar('Velocity deviation', abs(rand.normal())),
        StateVar('Latitude', rand.uniform(35, 45)),
        StateVar('Longitude', rand.uniform(100, 120)),
        StateVar('Missed pass count', rand.choice([0, 1, 2], p=[0.6, 0.3, 0.1]), kind='int'),
        StateVar('Year first seen', rand.randint(1980, 2020), kind='int'),
    ]
    return s


class Recommender:
    def __init__(self, state_type='space', clf_type='', max_n=1000):

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

    def step(self):
        if self.N == self.max_N:
            raise StopIteration('Max N reached')
        state = self.state_generator()
        state_vec = state2vec(state)
        try:
            # predict action with an associated probability
            pred_action = self.clf.predict(np.array(state_vec).reshape(1, -1))[0]
            probs = self.clf.predict_proba(np.array(state_vec).reshape(1, -1))[0]
            if len(probs) < self.action_size:
                probs = [1 / self.action_size] * self.action_size

        except NotFittedError:
            # first round we have no predictions
            pred_action, probs = 0, [1 / self.action_size] * self.action_size

        # logs
        self.N += 1
        self.states.append(state_vec)
        self.pred_history.append(pred_action)
        self.prob_history.append(probs)

        return state, pred_action, probs

    def train(self, action):
        """ We train after every action """
        self.actions.append(action)
        assert len(self.states) == len(self.actions),\
            'state-action mismatch - check calls to train() and step()'
        self.clf.fit(self.states, self.actions)
        if self.clf_type == 'tree':
            self.save_tree_graph()

    def reset(self):
        self.__init__(state_type=self.state_type, max_n=self.max_N, clf_type=self.clf_type)

    def save_tree_graph(self):
        export_graphviz(self.clf, out_file='static/images/tree_viz', class_names=ACTION_KEYS,
                        feature_names=STATE_KEYS, precision=1, rounded=True, filled=True,
                        impurity=False, label='none')
        plot_tree(self.clf, class_names=ACTION_KEYS, feature_names=STATE_KEYS, precision=1,
                  rounded=True, filled=True, impurity=False, label='none')
        plt.savefig('static/images/tree_graph')


if __name__ == '__main__':

    model = Recommender(max_n=10, state_type='space')
    for _ in range(model.max_N):
        s, pred, probs = model.step()
        print(f'Input:  {s}           '
              f'Predicted action: {pred}  ({[100 * p for p in probs]}% probability)')
        a = int(input('Action: '))
        model.train(a)
