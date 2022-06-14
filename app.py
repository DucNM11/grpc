#!/usr/bin/env python3

# Only import required modules/functions to optimize computing resources
from flask import Flask, flash, render_template, request, jsonify, redirect, url_for
from numpy import array, append
from time import perf_counter
import asyncio

from grpc_srv import client

# Initiate flask app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def check_size(matrix):
    """Function to check the matrix size (n x n) n is power of 2"""
    is_2n = lambda x: False if x == 0 else x & (x - 1) == 0

    matrix_shape = matrix.shape

    if len(matrix_shape) > 1:
        return  is_2n(matrix_shape[0]) \
                and is_2n(matrix_shape[1])
    else:
        return False


def parse_file(file):
    """Parse file to numpy 2d array"""
    parsed_string = file.read().decode('utf-8')
    if parsed_string[-1] == '\n':
        parsed_string = parsed_string[:-1]

    matrix = array([
        array(list(map(int, row.split(' '))))
        for row in parsed_string.split('\n')
    ])

    # 2d array being passed around is always in numpy array format, since numpy data storage size for list is more optimal than python list
    return matrix


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def get_matrix():
    # Get data from html form
    files = request.files.getlist('matrices[]')
    deadline = request.form.get("deadline", 30, int)
    operation = request.form.get("operation")

    if len(files) != 2:
        flash('Upload exactly two text files for the operation', 'error')
        return redirect(url_for('index_page'))

    matrix_1 = parse_file(files[0])
    matrix_2 = parse_file(files[1])

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

    time = perf_counter()

    if operation == 'add':
        rs = asyncio.run(client.as_add(matrix_1, matrix_2))
    else:
        rs = asyncio.run(client.as_lb_mul(matrix_1, matrix_2, deadline))

    total_time = perf_counter() - time
    print(f'Operation takes {total_time} seconds')

    return jsonify(success=err == 0,
                   operation=operation,
                   deadline=deadline,
                   runtime=total_time,
                   result=rs.tolist())


if __name__ == '__main__':
    app.run(debug=True)