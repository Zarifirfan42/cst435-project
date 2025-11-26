import grpc
from concurrent import futures
import pipeline_pb2
import pipeline_pb2_grpc

SVC3_ADDRESS = "svc3:50053"

class Svc2Servicer(pipeline_pb2_grpc.PipelineServiceServicer):
    def ProcessChunk(self, request, context):
        multiplied = [x*2 for x in request.numbers]
        # Call svc3
        stub_channel = grpc.insecure_channel(SVC3_ADDRESS)
        stub = pipeline_pb2_grpc.PipelineServiceStub(stub_channel)
        response = stub.ProcessChunk(pipeline_pb2.ChunkRequest(numbers=multiplied))
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pipeline_pb2_grpc.add_PipelineServiceServicer_to_server(Svc2Servicer(), server)
    server.add_insecure_port("[::]:50052")
    print("svc2 running on 50052")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
