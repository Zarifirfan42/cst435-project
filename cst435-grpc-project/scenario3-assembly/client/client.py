# scenario3-assembly/client/client.py
import grpc
import random
import pipeline_pb2
import pipeline_pb2_grpc
import time
from queue import Queue
from threading import Thread

SVC1_ADDRESS = "localhost:50051"

# Settings
random.seed(40)
NUM_CHUNKS = 10
CHUNK_SIZE = 10_000  # total 10 * 10k = 100k integers
NUM_ITEMS = NUM_CHUNKS * CHUNK_SIZE

def send_chunk(chunk, results_queue):
    with grpc.insecure_channel(SVC1_ADDRESS) as channel:
        stub = pipeline_pb2_grpc.PipelineServiceStub(channel)
        response = stub.ProcessChunk(pipeline_pb2.ChunkRequest(numbers=chunk))
        results_queue.put(response.sum)

if __name__ == "__main__":
    # Generate chunks (deterministic because of seed)
    chunks = [[random.randint(-10, 10) for _ in range(CHUNK_SIZE)] for _ in range(NUM_CHUNKS)]
    results_queue = Queue()

    start = time.perf_counter()

    # Feed chunks asynchronously into the single pipeline (assembly-line style)
    threads = []
    for chunk in chunks:
        t = Thread(target=send_chunk, args=(chunk, results_queue))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end = time.perf_counter()

    total_sum = sum([results_queue.get() for _ in range(NUM_CHUNKS)])
    total_time = end - start

    # Pipeline (per-chunk) metrics — what you've been measuring
    throughput_chunks_per_sec = NUM_CHUNKS / total_time
    items_per_sec_chunks = (NUM_CHUNKS * CHUNK_SIZE) / total_time

    # Full-dataset metrics — directly comparable with the simple client
    transaction_time_full = total_time                    # time to process full 100k through pipeline
    throughput_full_tx = 1.0 / transaction_time_full     # transactions/sec (where 1 transaction = full dataset)
    items_per_sec_full = NUM_ITEMS / transaction_time_full

    print("\n=== Assembly Pipeline Results ===")
    print(f"Final sum: {total_sum}\n")

    # Per-chunk / pipeline view
    print(">> Pipeline (per-chunk) view:")
    print(f"Total time (wall): {total_time:.4f} sec")
    print(f"Throughput: {throughput_chunks_per_sec:.2f} chunks/sec (chunks = {NUM_CHUNKS})")
    print(f"Throughput: {items_per_sec_chunks:.2f} items/sec\n")

    # Full-dataset (comparable to simple client)
    print(">> Full-dataset (comparable to simple client) view:")
    print(f"Transaction Time (full dataset): {transaction_time_full:.4f} sec")
    print(f"Throughput: {throughput_full_tx:.2f} transactions/sec (1 full dataset transaction)")
    print(f"Throughput: {items_per_sec_full:.2f} items/sec (for {NUM_ITEMS} items)\n")
