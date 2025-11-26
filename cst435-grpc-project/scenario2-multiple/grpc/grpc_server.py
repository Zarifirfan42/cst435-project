import grpc
from concurrent import futures
import compute_pb2
import compute_pb2_grpc

class ComputeServiceServicer(compute_pb2_grpc.ComputeServiceServicer):
    def SumSquares(self, request, context):
        result = sum(x*x for x in request.numbers)
        return compute_pb2.SumSquaresResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    compute_pb2_grpc.add_ComputeServiceServicer_to_server(
        ComputeServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    print("gRPC server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
