import grpc
import random
import pipeline_pb2
import pipeline_pb2_grpc
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

SVC1_ADDRESS = "localhost:50051"

# Set seed
random.seed(40)

NUM_CHUNKS = 10
CHUNK_SIZE = 10_000  # total 10*10k = 100k integers

def send_chunk(numbers):
    with grpc.insecure_channel(SVC1_ADDRESS) as channel:
        stub = pipeline_pb2_grpc.PipelineServiceStub(channel)
        response = stub.ProcessChunk(pipeline_pb2.ChunkRequest(numbers=numbers))
        return response.sum

if __name__ == "__main__":
    # Generate chunks
    chunks = [[random.randint(-10, 10) for _ in range(CHUNK_SIZE)] for _ in range(NUM_CHUNKS)]

    start = time.perf_counter()

    # Send all chunks concurrently
    results = []
    with ThreadPoolExecutor(max_workers=NUM_CHUNKS) as ex:
        futures = [ex.submit(send_chunk, chunk) for chunk in chunks]
        for fut in as_completed(futures):
            results.append(fut.result())

    end = time.perf_counter()

    total_sum = sum(results)
    total_time = end - start
    throughput_tx = NUM_CHUNKS / total_time
    throughput_items = (NUM_CHUNKS*CHUNK_SIZE) / total_time

    print("\n=== Benchmark Summary ===")
    print(f"Final sum: {total_sum}")
    print(f"Total time: {total_time:.4f} sec")
    print(f"Throughput: {throughput_tx:.2f} transactions/sec")
    print(f"Throughput: {throughput_items:.2f} items/sec")
