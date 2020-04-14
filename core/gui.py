import os
from pathlib import Path
from flask import Blueprint, request, redirect, url_for, flash, render_template, Response, session
from .recommender import Recommender, transform_space_state, STATE_KEYS, STATE_TYPES

bp = Blueprint('gui', __name__)
home_path = Path(__file__).parent


def reset():
    # clear images
    tree_img = home_path.joinpath('static', 'images', 'tree_graph.png')
    if os.path.isfile(tree_img):
        os.remove(tree_img)

    # init models
    session['models'] = {'simple': Recommender(state_type='simple'),
                         'space': Recommender(state_type='space')}


def format_space_state(state):
    state_dict = transform_space_state(state)
    formatted_state_list = []
    for i, k in enumerate(STATE_KEYS):
        if STATE_TYPES[i] == 'enum':
            val_str = state_dict[k]
        elif STATE_TYPES[i] == 'int':
            val_str = f'{state_dict[k]:.0f}'
        else:
            val_str = f'{state_dict[k]:.1f}'
        formatted_state_list.append((k, val_str))
    return formatted_state_list


@bp.route('/', methods=['GET'])
def landing():
    reset()
    # return render_template('gui/landing.html')
    return redirect(url_for('gui.main', env='space'))


@bp.route('/play/<env>', methods=['GET', 'POST'])
def main(env):
    if env == 'space':
        m = session['models']['space']
        template = 'gui/space.html'
    else:
        m = session['models']['simple']
        template = 'gui/simple.html'

    if len(m.states) == len(m.actions):
        s, pred_a, probs = m.display_next_state()
        m.states.append(s)
        m.pred_history.append(pred_a)
        m.prob_history.append(probs)
    else:
        s, pred_a, probs = m.states[-1], m.pred_history[-1], m.prob_history[-1]
    state_txt = format_space_state(s) if env == 'space' else s
    return render_template(template, env=env, state=state_txt, pred_action=pred_a, probabilities=probs,
                           N=m.N)


@bp.route('/act/<env>/<int:action>', methods=['POST'])
def act(env, action):
    m = session['models']['space'] if env == 'space' else session['models']['simple']
    m.actions.append(action)
    assert len(m.states) == len(m.actions), 'state action history mismatch'
    m.train()
    return redirect(url_for('gui.main', env=env))


@bp.route('/<env>/data', methods=['GET'])
def dump_data(env):
    """ Prints data to console """
    m = session['models']['space'] if env == 'space' else session['models']['simple']
    txt = f'States: {m.states}\nActions: {m.actions}'
    print(txt)
    return Response(txt, status=200)

