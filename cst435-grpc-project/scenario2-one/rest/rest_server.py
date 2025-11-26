from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SumRequest(BaseModel):
    numbers: list[int]

@app.post("/sumsquares")
def sum_squares(req: SumRequest):
    return {"result": sum(x*x for x in req.numbers)}

if __name__ == "__main__":
    import uvicorn
    print("REST server running on port 8000...")
    uvicorn.run("rest_server:app", host="0.0.0.0", port=8000)
