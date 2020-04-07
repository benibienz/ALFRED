from flask import Blueprint, request, redirect, url_for, flash, render_template, Response
from .expert import Expert, transform_space_state, STATE_KEYS, STATE_TYPES

bp = Blueprint('gui', __name__)
model = Expert(state_type='space')
states, actions, pred_hist, prob_hist = [], [], [], []
main_html = 'gui/space.html'


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


@bp.route('/', methods=['GET', 'POST'])
def main():
    if len(states) == len(actions):
        s, pred_a, probs = model.display_next_state()
        states.append(s)
        pred_hist.append(pred_a)
        prob_hist.append(probs)
    else:
        s, pred_a, probs = states[-1], pred_hist[-1], prob_hist[-1]
    state_txt = format_space_state(s)
    return render_template(main_html, state=state_txt, pred_action=pred_a, probabilities=probs)


@bp.route('/act/<int:action>', methods=['POST'])
def act(action):
    actions.append(action)
    assert len(states) == len(actions), 'state action history mismatch'
    model.train(states, actions)
    return redirect(url_for('gui.main'))


@bp.route('/data', methods=['GET'])
def dump_data():
    """ Prints data to console """
    txt = f'States: {states}\nActions: {actions}'
    print(txt)
    return Response(txt, status=200)

