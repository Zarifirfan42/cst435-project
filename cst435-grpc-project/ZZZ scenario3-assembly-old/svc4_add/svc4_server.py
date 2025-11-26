import grpc
from concurrent import futures
import pipeline_pb2
import pipeline_pb2_grpc

SVC5_ADDRESS = "svc5:50055"

class Svc4Servicer(pipeline_pb2_grpc.PipelineServiceServicer):
    def ProcessChunk(self, request, context):
        added = [x+1 for x in request.numbers]
        with grpc.insecure_channel(SVC5_ADDRESS) as channel:
            stub = pipeline_pb2_grpc.PipelineServiceStub(channel)
            response = stub.ProcessChunk(pipeline_pb2.ChunkRequest(numbers=added))
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pipeline_pb2_grpc.add_PipelineServiceServicer_to_server(Svc4Servicer(), server)
    server.add_insecure_port("[::]:50054")
    print("svc4 running on 50054")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
