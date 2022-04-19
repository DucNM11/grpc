from common import to_grpc_matrix, to_matrix
from random import randrange
from numpy import matmul, array, random, zeros, savetxt
from time import perf_counter, sleep
import asyncio

import grpc
import service_pb2 as pb2
import service_pb2_grpc as pb2_grpc


def mul(a, b):
    with grpc.insecure_channel('34.67.215.11:8888') as channel:
        stub = pb2_grpc.CalStub(channel)
        response = stub.mul_matrix(
            pb2.request_msg(matrix_1=to_grpc_matrix(a),
                            matrix_2=to_grpc_matrix(b)))

    return to_matrix(response.result)


async def s_mul(a, b):
    async with grpc.aio.insecure_channel('34.67.215.11:8888') as channel:
        stub = pb2_grpc.CalStub(channel)
        response = await stub.mul_matrix(
            pb2.request_msg(matrix_1=to_grpc_matrix(a),
                            matrix_2=to_grpc_matrix(b)))

    return to_matrix(response.result)


def rec_mul(a, b):
    n = len(a)

    if n <= 2**5:
        rs = array(mul(a, b))
    else:

        split = int(n / 2)

        a00 = a[:split, :split]
        a01 = a[:split, split:]
        a10 = a[split:, :split]
        a11 = a[split:, split:]

        b00 = b[:split, :split]
        b01 = b[:split, split:]
        b10 = b[split:, :split]
        b11 = b[split:, split:]

        c00 = rec_mul(a00, b00) + rec_mul(a01, b10)
        c01 = rec_mul(a00, b01) + rec_mul(a01, b11)
        c10 = rec_mul(a10, b00) + rec_mul(a11, b10)
        c11 = rec_mul(a11, b11) + rec_mul(a10, b01)

        rs = zeros(shape=(n, n))

        rs[:split, :split] = c00
        rs[:split, split:] = c01
        rs[split:, :split] = c10
        rs[split:, split:] = c11

    return rs


async def s_rec_mul(a, b):
    n = len(a)

    if n <= 2**5:
        rs = array(await s_mul(a, b))
    else:

        split = int(n / 2)

        a00 = a[:split, :split]
        a01 = a[:split, split:]
        a10 = a[split:, :split]
        a11 = a[split:, split:]

        b00 = b[:split, :split]
        b01 = b[:split, split:]
        b10 = b[split:, :split]
        b11 = b[split:, split:]

        c00 = await s_rec_mul(a00, b00) + await s_rec_mul(a01, b10)
        c01 = await s_rec_mul(a00, b01) + await s_rec_mul(a01, b11)
        c10 = await s_rec_mul(a10, b00) + await s_rec_mul(a11, b10)
        c11 = await s_rec_mul(a11, b11) + await s_rec_mul(a10, b01)

        rs = zeros(shape=(n, n))

        rs[:split, :split] = c00
        rs[:split, split:] = c01
        rs[split:, :split] = c10
        rs[split:, split:] = c11

    return rs


arr = random.randint(1, 100, size=(2**6, 2**6))

# mul(arr, arr)

start = perf_counter()

rec_mul(arr, arr)

print(perf_counter() - start)

# start = perf_counter()

# asyncio.run(s_rec_mul(arr, arr))

# print(perf_counter() - start)

# start = perf_counter()

# mul(arr, arr)

# print(perf_counter() - start)
