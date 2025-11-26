import xmlrpc.client

def xmlrpc_sum_squares(numbers):
    proxy = xmlrpc.client.ServerProxy("http://localhost:9000")
    return proxy.sum_squares(numbers)

if __name__ == "__main__":
    import random
    nums = [random.randint(1, 10) for _ in range(100000)]
    print("XML-RPC Sum of squares:", xmlrpc_sum_squares(nums))
