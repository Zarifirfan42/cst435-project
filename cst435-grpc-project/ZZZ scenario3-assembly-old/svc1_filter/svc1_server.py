import grpc
from concurrent import futures
import pipeline_pb2
import pipeline_pb2_grpc

import time

SVC2_ADDRESS = "svc2:50052"

class Svc1Servicer(pipeline_pb2_grpc.PipelineServiceServicer):
    def ProcessChunk(self, request, context):
        filtered = [x for x in request.numbers if x > 0]

        # Call svc2
        with grpc.insecure_channel(SVC2_ADDRESS) as channel:
            stub = pipeline_pb2_grpc.PipelineServiceStub(channel)
            response = stub.ProcessChunk(pipeline_pb2.ChunkRequest(numbers=filtered))
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pipeline_pb2_grpc.add_PipelineServiceServicer_to_server(Svc1Servicer(), server)
    server.add_insecure_port("[::]:50051")
    print("svc1 running on 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
