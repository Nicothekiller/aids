from concurrent import futures

import grpc

import aids_pb2_grpc
from api import AidsServiceServicer


def serve():
    """Starts the gRPC server and waits for requests."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aids_pb2_grpc.add_AidsServiceServicer_to_server(AidsServiceServicer(), server)
    port = server.add_insecure_port("[::]:50051")
    server.start()
    print(f"Server started, listening on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

