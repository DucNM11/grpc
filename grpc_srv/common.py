from numpy import array

# Using try except to make sure this script could be called independently or through flask app (from different dir)
try:
    import service_pb2 as pb2
except:
    import grpc_srv.service_pb2 as pb2


def to_grpc_matrix(matrix):
    grpc_matrix = pb2.matrix()

    for row in matrix:
        grpc_row = [pb2.row(value=row.tolist())]
        grpc_matrix.row.extend(grpc_row)

    return grpc_matrix


def to_matrix(matrix):

    list_matrix = []
    for row in matrix.row:
        list_matrix.append([val for val in row.value])

    np_matrix = array(list_matrix)

    return np_matrix