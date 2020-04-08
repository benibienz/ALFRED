from flask import Blueprint, request, redirect, url_for, flash, render_template, Response
from .expert import Expert, transform_space_state, STATE_KEYS, STATE_TYPES

bp = Blueprint('gui', __name__)
models = {'simple': Expert(state_type='simple'),
          'space': Expert(state_type='space')}


def format_space_state(state):
    state_dict = transform_space_state(state)
    formatted_state_list = []
    print(state_dict)
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
    models['simple'].reset()
    models['space'].reset()
    return render_template('gui/landing.html')


@bp.route('/<env>', methods=['GET', 'POST'])
def main(env):
    if env == 'space':
        m = models['space']
        template = 'gui/space.html'
    else:
        m = models['simple']
        template = 'gui/simple.html'

    if len(m.states) == len(m.actions):
        s, pred_a, probs = m.display_next_state()
        m.states.append(s)
        m.pred_hist.append(pred_a)
        m.prob_hist.append(probs)
    else:
        s, pred_a, probs = m.states[-1], m.pred_hist[-1], m.prob_hist[-1]
    state_txt = format_space_state(s) if env == 'space' else s
    return render_template(template, env=env, state=state_txt, pred_action=pred_a, probabilities=probs)


@bp.route('/act/<env>/<int:action>', methods=['POST'])
def act(env, action):
    m = models['space'] if env == 'space' else models['simple']
    m.actions.append(action)
    assert len(m.states) == len(m.actions), 'state action history mismatch'
    m.train()
    return redirect(url_for('gui.main', env=env))


@bp.route('/<env>/data', methods=['GET'])
def dump_data(env):
    """ Prints data to console """
    m = models['space'] if env == 'space' else models['simple']
    txt = f'States: {m.states}\nActions: {m.actions}'
    print(txt)
    return Response(txt, status=200)

