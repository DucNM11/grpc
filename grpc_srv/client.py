#!/usr/bin/env python3

# Import needed modules/functions only to optimize computing resources
from numpy import random, zeros, savetxt
from random import choice
from time import perf_counter, sleep
import asyncio

# Import grpc related classes/package
import grpc

# Using try except to make sure this script could be called independently or through flask app (from different dir)
try:
    from common import to_grpc_matrix, to_matrix
    import service_pb2 as pb2
    import service_pb2_grpc as pb2_grpc
except:
    from grpc_srv.common import to_grpc_matrix, to_matrix
    import grpc_srv.service_pb2 as pb2
    import grpc_srv.service_pb2_grpc as pb2_grpc

options = [('grpc.max_send_message_length', 1024**3),
           ('grpc.max_receive_message_length', 1024**3)]

# IP list of servers for client-side load-balancing
srv_list = [
    '35.184.147.23', '104.197.121.61', '35.188.32.59', '34.67.216.44',
    '35.193.28.160', '104.154.201.221', '34.123.28.141', '34.67.215.11'
]


# ASynchronous MULtiplication request
async def as_mul(a, b, srv=choice(srv_list)):
    """Request multiplication operation from grpc server"""
    print(f'multiply with srv {srv}')
    async with grpc.aio.insecure_channel(f'{srv}:80',
                                         options=options) as channel:
        stub = pb2_grpc.CalStub(channel)
        response = await stub.mul_matrix(
            pb2.request_msg(matrix_1=to_grpc_matrix(a),
                            matrix_2=to_grpc_matrix(b)))

    return to_matrix(response.result)


# ASynchronous ADDition request
async def as_add(a, b, srv=choice(srv_list)):
    """Request addition operation from grpc server"""
    print(f'add with srv {srv}')
    async with grpc.aio.insecure_channel(f'{srv}:80',
                                         options=options) as channel:
        stub = pb2_grpc.CalStub(channel)
        response = await stub.add_matrix(
            pb2.request_msg(matrix_1=to_grpc_matrix(a),
                            matrix_2=to_grpc_matrix(b)))

    return to_matrix(response.result)


# ASynchronous Load-Balanced MULtiplication
async def as_lb_mul(a, b, deadline):
    """Navie divide and conquer with no recursion"""
    n = len(a)

    split = int(n / 2)

    a00 = a[:split, :split]
    a01 = a[:split, split:]
    a10 = a[split:, :split]
    a11 = a[split:, split:]

    b00 = b[:split, :split]
    b01 = b[:split, split:]
    b10 = b[split:, :split]
    b11 = b[split:, split:]

    computation_list = [(a00, b00), (a01, b10), (a00, b01), (a01, b11),
                        (a10, b00), (a11, b10), (a11, b11), (a10, b01)]

    start = perf_counter()

    # Randomized the server for footprinting to assure load - balancing
    timer = await as_mul(a00, b00, choice(srv_list))

    total_time = perf_counter() - start

    # 12 sub operations in total consists of 8 multiplications and 4 additions
    total_srv = min(
        len(srv_list),
        int((-(-total_time * 12) // deadline)) +
        1)  # // Deadline - Tenichique to round up without external package

    print(
        f'Footprinting - One request takes {total_time} seconds, we will utilize {total_srv} servers for this task'
    )

    params = []
    for i, param in enumerate(computation_list):
        params.append([param[0], param[1], srv_list[i % total_srv]])

    # Using asynchronous call to optimmize performance
    s_call = asyncio.gather(*[as_mul(a, b, port) for (a, b, port) in params])
    rs = await s_call

    del params
    params = []
    for i in range(0, 8, 2):
        params.append([rs[i], rs[i + 1], srv_list[(i // 2) % total_srv]])

    # Using asynchronous call to optimmize performance
    rs_add = asyncio.gather(*[as_add(a, b, port) for (a, b, port) in params])

    del rs
    tmp_rs = await rs_add

    rs = zeros(shape=(n, n))

    rs[:split, :split] = tmp_rs[0]
    rs[:split, split:] = tmp_rs[1]
    rs[split:, :split] = tmp_rs[2]
    rs[split:, split:] = tmp_rs[3]

    return rs
