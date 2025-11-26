import grpc
from concurrent import futures
import pipeline_pb2
import pipeline_pb2_grpc
from concurrent.futures import ThreadPoolExecutor

SVC3_ADDRESS = "svc3:50053"

class Svc2Servicer(pipeline_pb2_grpc.PipelineServiceServicer):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=5)

    def ProcessChunk(self, request, context):
        future = self.executor.submit(self.handle_chunk, request)
        return future.result()

    def handle_chunk(self, request):
        multiplied = [x*2 for x in request.numbers]
        with grpc.insecure_channel(SVC3_ADDRESS) as channel:
            stub = pipeline_pb2_grpc.PipelineServiceStub(channel)
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
