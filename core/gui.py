import os
from pathlib import Path
from flask import Blueprint, request, redirect, url_for, render_template, Response, session, jsonify
from .recommender import Recommender, transform_space_state, STATE_KEYS, STATE_TYPES, ACTION_NAMES

bp = Blueprint('gui', __name__)
home_path = Path(__file__).parent


def reset():
    """ New models, clear everything """
    # clear images
    tree_img = home_path.joinpath('static', 'images', 'tree_graph.png')
    if os.path.isfile(tree_img):
        os.remove(tree_img)

    # init models
    session['models'] = {'simple': Recommender(state_type='simple'),
                         'space': Recommender(state_type='space')}


def format_space_state(state):
    """
    Formats space state for html template
    Args:
        state: numerical state array from model

    Returns: list of formatted strings
    """
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


def format_probs(probs):
    """
    Format probabilities array for html template
    Args:
        probs: probs array from model

    Returns: list of rounded floats
    """
    return [round(p, 2) for p in probs]


@bp.route('/', methods=['GET'])
def landing():
    # rerouting this to space demo for now
    # reset()
    # return render_template('gui/landing.html')
    return redirect(url_for('gui.main', env='space'))


@bp.route('/play/<env>', methods=['GET'])
def main(env):
    """
    The view for the main app.
    Args:
        env: 'space' or 'simple' (just space for now)
    """
    reset()
    if env == 'space':
        m = session['models']['space']
        template = 'gui/space.html'
    else:
        m = session['models']['simple']
        template = 'gui/simple.html'

    s, pred_a, probs = m.step()
    state_txt = format_space_state(s) if env == 'space' else s
    return render_template(template, env=env, state=state_txt, actions=ACTION_NAMES)


@bp.route('/act', methods=['POST'])
def act():
    """ Action endpoint """
    # get action from request and train model
    action = request.form['action']
    env = request.form['env']
    m = session['models']['space'] if env == 'space' else session['models']['simple']
    m.train(action)

    # step to next state and return state vector and recommended action
    s, pred_a, probs = m.step()
    state_txt = format_space_state(s) if env == 'space' else s
    return jsonify({'state': state_txt, 'pred_action': pred_a, 'probs': format_probs(probs)})
