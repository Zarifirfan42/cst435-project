import grpc
from concurrent import futures
import pipeline_pb2
import pipeline_pb2_grpc

SVC4_ADDRESS = "svc4:50054"

class Svc3Servicer(pipeline_pb2_grpc.PipelineServiceServicer):
    def ProcessChunk(self, request, context):
        squared = [x*x for x in request.numbers]
        with grpc.insecure_channel(SVC4_ADDRESS) as channel:
            stub = pipeline_pb2_grpc.PipelineServiceStub(channel)
            response = stub.ProcessChunk(pipeline_pb2.ChunkRequest(numbers=squared))
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pipeline_pb2_grpc.add_PipelineServiceServicer_to_server(Svc3Servicer(), server)
    server.add_insecure_port("[::]:50053")
    print("svc3 running on 50053")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
