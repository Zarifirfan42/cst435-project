# concurrent

import random
import time
import grpc
import httpx
import xmlrpc.client
import compute_pb2
import compute_pb2_grpc
from concurrent.futures import ThreadPoolExecutor, as_completed

# Worker addresses
GRPC_WORKERS = ["localhost:50051", "localhost:50052", "localhost:50053",
                "localhost:50054", "localhost:50055"]

REST_WORKERS = ["http://localhost:8001/sumsquares",
                "http://localhost:8002/sumsquares",
                "http://localhost:8003/sumsquares",
                "http://localhost:8004/sumsquares",
                "http://localhost:8005/sumsquares"]

XMLRPC_WORKERS = ["http://localhost:9001",
                  "http://localhost:9002",
                  "http://localhost:9003",
                  "http://localhost:9004",
                  "http://localhost:9005"]

def grpc_sum_squares_worker(numbers, address):
    channel = grpc.insecure_channel(address)
    stub = compute_pb2_grpc.ComputeServiceStub(channel)
    request = compute_pb2.SumSquaresRequest(numbers=numbers)
    response = stub.SumSquares(request)
    return response.result

def rest_sum_squares_worker(numbers, url):
    resp = httpx.post(url, json={"numbers": numbers}, timeout=60)
    return resp.json()["result"]

def xmlrpc_sum_squares_worker(numbers, url):
    proxy = xmlrpc.client.ServerProxy(url)
    return proxy.sum_squares(numbers)

def run_concurrent(func, workers, numbers):
    num_workers = len(workers)
    chunks = [numbers[i::num_workers] for i in range(num_workers)]

    results = [None] * num_workers
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_workers) as ex:
        futures = {ex.submit(func, chunks[i], workers[i]): i for i in range(num_workers)}
        for fut in as_completed(futures):
            i = futures[fut]
            results[i] = fut.result()
    end = time.perf_counter()
    total = sum(results)
    total_time = end - start
    throughput_tx = 1 / total_time
    throughput_items = len(numbers) / total_time

    print(f"Result: {total}")
    print(f"Total Time: {total_time:.4f} sec")
    print(f"Throughput: {throughput_tx:.2f} transactions/sec")
    print(f"Throughput: {throughput_items:.2f} items/sec\n")

if __name__ == "__main__":
    random.seed(40)
    numbers = [random.randint(1, 10) for _ in range(100000)]

    print("=== gRPC Multi-Worker Concurrent ===")
    run_concurrent(grpc_sum_squares_worker, GRPC_WORKERS, numbers)

    print("=== REST Multi-Worker Concurrent ===")
    run_concurrent(rest_sum_squares_worker, REST_WORKERS, numbers)

    print("=== XML-RPC Multi-Worker Concurrent ===")
    run_concurrent(xmlrpc_sum_squares_worker, XMLRPC_WORKERS, numbers)