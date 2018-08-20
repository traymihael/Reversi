
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import reversi


app = Flask(__name__)


# 初回はこちらにアクセス
@app.route('/')
def index():
    return render_template('index.html', line=locate_list, title=title,
                           width = width, position_data=position_data, turn=turn, judge=judge)


# /post にアクセスしたときの処理（2回目以降はこちら）
@app.route('/post', methods=['GET', 'POST'])
def post():
    global locate_list, turn, history

    location = request.args.get('get_value')
    if location == 'already':
        judge = 'ng'
    elif reversi.check(locate_list, location, turn):
        locate_list = reversi.change_bord(locate_list, location, turn)
        history = reversi.get_hist(history, location, turn)
        turn = reversi.change_turn(turn)
        judge = 'ok'
    else:
        judge = 'ng'

    if reversi.check_next(locate_list, turn) == 0:
        turn = reversi.change_turn(turn)
        if reversi.check_next(locate_list, turn) == 0:
            judge = 'finish'


    return render_template('index.html', line=locate_list, title=title,
                           width=width, position_data=position_data, turn=turn, judge=judge)


@app.route('/undo', methods=['GET', 'POST'])
def undo():
    global locate_list, turn, history

    locate_list, history = reversi.undo_data(locate_list, history)
    turn = reversi.change_turn(turn)
    judge = 'start'

    return render_template('index.html', line= locate_list, title=title,
                           width = width, position_data=position_data, turn=turn, judge=judge)


@app.route('/restart', methods=['GET', 'POST'])
def restart():
    global locate_list, turn, history
    locate_list = reversi.get_initial_place()
    history = []
    turn = 'b'
    judge = 'start'
    return render_template('index.html', line=locate_list, title=title,
                           width=width, position_data=position_data, turn=turn, judge=judge)


if __name__ == '__main__':
    # コマ情報を保持
    locate_list = reversi.get_initial_place()
    position_data = reversi.get_position()
    width = [_ for _ in range(8)]
    history = []
    turn = 'b'
    judge = 'start'


    title = 'REVERSI'

    app.debug = True
    app.run(host='0.0.0.0', port=8000)
