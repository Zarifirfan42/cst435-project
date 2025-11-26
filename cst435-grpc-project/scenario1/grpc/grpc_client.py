import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../grpc")))

import grpc
import compute_pb2
import compute_pb2_grpc

def grpc_sum_squares(numbers):
    channel = grpc.insecure_channel("localhost:50051")
    stub = compute_pb2_grpc.ComputeServiceStub(channel)
    request = compute_pb2.SumSquaresRequest(numbers=numbers)
    response = stub.SumSquares(request)
    return response.result

if __name__ == "__main__":
    import random
    nums = [random.randint(1, 10) for _ in range(100000)]
    result = grpc_sum_squares(nums)
    print("gRPC Sum of squares:", result)
