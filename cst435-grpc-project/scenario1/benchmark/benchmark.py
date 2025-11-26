import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import time
import random

from scenario1.grpc.grpc_client import grpc_sum_squares
from scenario1.rest.rest_client import rest_sum_squares
from scenario1.xmlrpc.xmlrpc_client import xmlrpc_sum_squares

TRANSACTIONS = 50

def benchmark(func, numbers, transactions=TRANSACTIONS):
    times = []
    for _ in range(transactions):
        start = time.perf_counter()
        func(numbers)
        end = time.perf_counter()
        times.append(end - start)
    total_time = sum(times)
    avg_time = total_time / transactions
    throughput_tx = 1 / avg_time  # transactions/sec
    throughput_items = len(numbers) / avg_time  # items/sec

    print(f"Total Transactions: {transactions}")
    print(f"Total Time: {total_time:.4f} seconds")
    print(f"Average Transaction Time: {avg_time:.4f} seconds")
    print(f"Throughput: {throughput_tx:.2f} transactions/sec")
    print(f"Throughput: {throughput_items:.2f} items/sec\n")

if __name__ == "__main__":
    numbers = [random.randint(1, 10) for _ in range(100000)]

    print("Benchmarking gRPC...")
    benchmark(grpc_sum_squares, numbers)

    print("Benchmarking REST...")
    benchmark(rest_sum_squares, numbers)

    print("Benchmarking XML-RPC...")
    benchmark(xmlrpc_sum_squares, numbers)
