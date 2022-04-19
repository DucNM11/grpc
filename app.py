#!/usr/bin/env python3

from flask import Flask, flash, render_template, request, jsonify, redirect, url_for
from numpy import array, append

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def check_size(matrix):

    is_2n = lambda x: False if x == 0 else x & (x - 1) == 0

    matrix_shape = matrix.shape

    if len(matrix_shape) > 1:
        return  is_2n(matrix_shape[0]) \
                and is_2n(matrix_shape[1])
    else:
        return False


def parse_file(file):
    parsed_string = file.read().decode('utf-8')
    if parsed_string[-1] == '\n':
        parsed_string = parsed_string[:-1]

    matrix = array([
        array(list(map(int, row.split(' '))))
        for row in parsed_string.split('\n')
    ])

    return matrix


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def get_matrix():
    files = request.files.getlist('matrices[]')

    if len(files) != 2:
        flash('Upload exactly two text files for the operation', 'error')
        return redirect(url_for('index_page'))

    matrix_1 = parse_file(files[0])
    matrix_2 = parse_file(files[1])
    deadline = request.form.get("deadline", 30, int)
    operation = request.form.get("operation")

    err = 0
    if not check_size(matrix_1):
        err += 1
    if not check_size(matrix_2):
        err += 2

    if err != 0:
        if err == 1:
            msg = files[0].filename
        elif err == 2:
            msg = files[1].filename
        elif err == 3:
            msg = 'boh files'
        flash(f'Invalid matrix. Please check {msg}', 'error')
        return redirect(url_for('index_page'))

    return jsonify(success=err,
                   matrix_1=matrix_1.tolist(),
                   matrix_2=matrix_2.tolist(),
                   deadline=deadline,
                   operation=operation)


if __name__ == '__main__':
    app.run(debug=True)