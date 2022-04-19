from common import to_grpc_matrix, to_matrix
from numpy import matmul, array
# import asyncio

import grpc
import service_pb2 as pb2
import service_pb2_grpc as pb2_grpc


class Matrix(pb2_grpc.CalServicer):

    def add_matrix(self, request, context):
        result = to_matrix(request.matrix_1) + to_matrix(request.matrix_2)

        return pb2.response_msg(result=to_grpc_matrix(result))

    def mul_matrix(self, request, context):
        result = matmul(to_matrix(request.matrix_1),
                        to_matrix(request.matrix_2))

        return pb2.response_msg(result=to_grpc_matrix(result))


def serve():
    server = grpc.server()
    pb2_grpc.add_CalServicer_to_server(Matrix(), server)
    server.add_insecure_port('[::]:8888')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()