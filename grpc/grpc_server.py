from common import to_grpc_matrix, to_matrix
from numpy import matmul, array
import asyncio

import grpc
import service_pb2 as pb2
import service_pb2_grpc as pb2_grpc

options = [('grpc.max_send_message_length', 1024**3),
           ('grpc.max_receive_message_length', 1024**3)]


class Matrix(pb2_grpc.CalServicer):

    async def add_matrix(self, request, context):
        result = to_matrix(request.matrix_1) + to_matrix(request.matrix_2)

        return pb2.response_msg(result=to_grpc_matrix(result))

    async def mul_matrix(
            self, request,
            context: grpc.aio.ServicerContext) -> pb2.response_msg:
        result = matmul(to_matrix(request.matrix_1),
                        to_matrix(request.matrix_2))

        return pb2.response_msg(result=to_grpc_matrix(result))


async def serve():
    server = grpc.aio.server(options=options)
    pb2_grpc.add_CalServicer_to_server(Matrix(), server)
    server.add_insecure_port('[::]:8888')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())