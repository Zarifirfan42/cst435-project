import httpx

def rest_sum_squares(numbers):
    resp = httpx.post("http://localhost:8000/sumsquares", json={"numbers": numbers})
    return resp.json()["result"]

if __name__ == "__main__":
    import random
    nums = [random.randint(1, 10) for _ in range(100000)]
    print("REST Sum of squares:", rest_sum_squares(nums))
