import grpc
import random
import pipeline_pb2
import pipeline_pb2_grpc
import time

SVC1_ADDRESS = "localhost:50051"

# Set seed
random.seed(40)

NUM_ITEMS = 100_000  # total integers

def run_pipeline(numbers):
    channel = grpc.insecure_channel(SVC1_ADDRESS)
    stub = pipeline_pb2_grpc.PipelineServiceStub(channel)
    response = stub.ProcessChunk(pipeline_pb2.ChunkRequest(numbers=numbers))
    return response.sum

if __name__ == "__main__":
    numbers = [random.randint(-10, 10) for _ in range(NUM_ITEMS)]

    start = time.perf_counter()
    total = run_pipeline(numbers)
    end = time.perf_counter()

    transaction_time = end - start
    throughput_tx = 1 / transaction_time
    throughput_items = NUM_ITEMS / transaction_time

    print("\n=== Benchmark Summary ===")
    print(f"Final sum: {total}")
    print(f"Transaction Time: {transaction_time:.4f} sec")
    print(f"Throughput: {throughput_tx:.2f} transactions/sec")
    print(f"Throughput: {throughput_items:.2f} items/sec")
