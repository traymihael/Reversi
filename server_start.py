
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import reversi


app = Flask(__name__)


# 初回はこちらにアクセス
@app.route('/')
def index():
    return render_template('index.html', line=locate_list, title='HOHOHO')

# /post にアクセスしたときの処理（2回目以降はこちら）
@app.route('/post', methods=['GET', 'POST'])
def post():
    global locate_list
    if request.method == 'POST':
        point_inf = request.form['point_inf']
        locate_list = reversi.put_koma(locate_list, point_inf)
        return render_template('index.html', line= locate_list, title='hogehoge')
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    # コマ情報を保持
    locate_list = reversi.get_initial_place()

    app.debug = True
    app.run(host='0.0.0.0', port=8000)
