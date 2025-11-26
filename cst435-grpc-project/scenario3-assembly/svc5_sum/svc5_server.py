import grpc
from concurrent import futures
import pipeline_pb2
import pipeline_pb2_grpc
from concurrent.futures import ThreadPoolExecutor

class Svc5Servicer(pipeline_pb2_grpc.PipelineServiceServicer):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=5)

    def ProcessChunk(self, request, context):
        future = self.executor.submit(self.handle_chunk, request)
        return future.result()

    def handle_chunk(self, request):
        total = sum(request.numbers)
        return pipeline_pb2.ChunkResponse(numbers=request.numbers, sum=total)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pipeline_pb2_grpc.add_PipelineServiceServicer_to_server(Svc5Servicer(), server)
    server.add_insecure_port("[::]:50055")
    print("svc5 running on 50055")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
