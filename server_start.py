
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import reversi
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('start.html')

@app.route('/vs_cp')
def vs_cp():
    return render_template('select_turn.html')

@app.route('/vs_cp_play')
def vs_cp_play():
    global locate_list, turn, history, cp_turn, judge
    turn = request.args.get('turn_value')
    if turn == 'w':
        cp_turn = 'b'
        location = reversi.where_put(locate_list, cp_turn)
        # print(locate_list)
        locate_list = reversi.change_bord(locate_list, location, cp_turn)
        history = reversi.get_hist(history, location, cp_turn)
        judge = 'ok'

    else:
        cp_turn = 'w'
    return render_template('vs_cp.html', line=locate_list, title=title,
                           width=width, position_data=position_data, turn=turn, judge=judge)




@app.route('/vs_cp_play_next')
def vs_cp_play_next():
    global locate_list, turn, history, cp_turn, judge
    location = request.args.get('get_value')
    # print(location)
    if location == 'already':
        judge = 'ng'
    elif reversi.check(locate_list, location, turn):
        locate_list = reversi.change_bord(locate_list, location, turn)
        history = reversi.get_hist(history, location, turn)
        judge = 'ok'
    else:
        judge = 'ng'


    if reversi.check_next(locate_list, cp_turn) == 0:
        judge = 'pass'
        if reversi.check_next(locate_list, turn) == 0:
            judge = 'finish'

    judge_list = ['finish', 'pass', 'ng']
    if judge not in judge_list:

        # render_template('vs_cp.html', line=locate_list, title=title,
        #                 width=width, position_data=position_data, turn=turn, judge=judge)
        # time.sleep(3)

        while 1:
            location = reversi.where_put(locate_list, cp_turn)
            # location = reversi.where_put_full_search(locate_list, cp_turn)

            locate_list = reversi.change_bord(locate_list, location, cp_turn)
            history = reversi.get_hist(history, location, cp_turn)
            judge = 'ok'

            if reversi.check_next(locate_list, turn) == 0:
                if reversi.check_next(locate_list, cp_turn) == 0:
                    judge = 'finish'
                    break
            else:
                break


    return render_template('vs_cp.html', line=locate_list, title=title,
                           width=width, position_data=position_data, turn=turn, judge=judge)

@app.route('/vs_cp_undo', methods=['GET', 'POST'])
def vs_cp_undo():
    global locate_list, turn, history
    locate_list, history = reversi.undo_data(locate_list, history[:-1])
    judge = 'start'

    return render_template('vs_cp.html', line= locate_list, title=title,
                           width = width, position_data=position_data, turn=turn, judge=judge)


@app.route('/vs_cp_restart', methods=['GET', 'POST'])
def vs_cp_restart():
    global locate_list, turn, history
    locate_list = reversi.get_initial_place()
    history = []
    judge = 'start'
    return render_template('vs_cp.html', line=locate_list, title=title,
                           width=width, position_data=position_data, turn=turn, judge=judge)


# 二人プレイにアクセスした時
@app.route('/vs_peaple')
def vs_people():
    return render_template('index.html', line=locate_list, title=title,
                           width = width, position_data=position_data, turn=turn, judge=judge)


# 2人プレイにアクセスしたときの処理（2回目以降はこちら）
@app.route('/vs_people_play', methods=['GET', 'POST'])
def vs_peaole_play():
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


@app.route('/vs_people_undo', methods=['GET', 'POST'])
def vs_people_undo():
    global locate_list, turn, history

    locate_list, history = reversi.undo_data(locate_list, history)
    turn = reversi.change_turn(turn)
    judge = 'start'

    return render_template('index.html', line= locate_list, title=title,
                           width = width, position_data=position_data, turn=turn, judge=judge)


@app.route('/vs_people_restart', methods=['GET', 'POST'])
def vs_people_restart():
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
    width = [_ for _ in range(4)]
    history = []
    turn = 'b'
    cp_turn = 'w'
    judge = 'start'


    title = 'REVERSI'

    app.debug = True
    app.run(host='0.0.0.0', port=8000)
