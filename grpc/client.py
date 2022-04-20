from common import to_grpc_matrix, to_matrix
from numpy import random, zeros, savetxt
from time import perf_counter, sleep
import asyncio

import grpc
import service_pb2 as pb2
import service_pb2_grpc as pb2_grpc

options = [('grpc.max_send_message_length', 1024**3),
           ('grpc.max_receive_message_length', 1024**3)]


async def s_mul(a, b, srv):
    print(f'multiply with srv {srv}')
    async with grpc.aio.insecure_channel(f'{srv}:80',
                                         options=options) as channel:
        stub = pb2_grpc.CalStub(channel)
        response = await stub.mul_matrix(
            pb2.request_msg(matrix_1=to_grpc_matrix(a),
                            matrix_2=to_grpc_matrix(b)))

    return to_matrix(response.result)


async def s_add(a, b, srv):
    print(f'add with srv {srv}')
    async with grpc.aio.insecure_channel(f'{srv}:80',
                                         options=options) as channel:
        stub = pb2_grpc.CalStub(channel)
        response = await stub.add_matrix(
            pb2.request_msg(matrix_1=to_grpc_matrix(a),
                            matrix_2=to_grpc_matrix(b)))

    return to_matrix(response.result)


async def s_rec_mul(a, b, deadline):
    global request_size
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
    # srv_list = list(range(8880, 8888))
    srv_list = [
        '35.184.147.23', '104.197.121.61', '104.154.201.221', '34.67.216.44',
        '34.123.28.141', '34.67.215.11', '35.188.32.59', '35.193.28.160'
    ]
    start = perf_counter()

    timer = await s_mul(a00, b00, srv_list[0])

    total_time = perf_counter() - start

    # In spite of having 12 operations in total with 8 multiplication and 4 addition
    # Since all operation running asynchronously multiply the footprinting total_time
    # for 12 will make it overestimates too much. By running multiple times, the most
    # accurate number for estimating in this case is 5.
    total_node = min(len(srv_list), round((total_time * 12) / deadline) + 1)

    params = []
    for i, param in enumerate(computation_list):
        params.append([param[0], param[1], srv_list[i % total_node]])

    s_call = asyncio.gather(*[s_mul(a, b, port) for (a, b, port) in params])
    rs = await s_call

    del params
    params = []
    for i in range(0, 8, 2):
        params.append([rs[i], rs[i + 1], srv_list[(i // 2) % total_node]])

    rs_add = asyncio.gather(*[s_add(a, b, port) for (a, b, port) in params])

    del rs
    tmp_rs = await rs_add

    rs = zeros(shape=(n, n))

    rs[:split, :split] = tmp_rs[0]
    rs[:split, split:] = tmp_rs[1]
    rs[split:, :split] = tmp_rs[2]
    rs[split:, split:] = tmp_rs[3]

    return rs


arr = random.randint(1, 100, size=(2**10, 2**10))

start = perf_counter()

asyncio.run(s_rec_mul(arr, arr, 5))

print(perf_counter() - start)
