from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Vercel URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FirstRow(BaseModel):
    row: List[int]

@app.post("/generate")
def generate_magic_square(data: FirstRow):
    dob = data.row
    if len(dob) != 4 or any(not (1 <= x < 100) for x in dob):
        return {"error": "Invalid input"}

    target_sum = sum(dob)
    used = set(dob)

    for _ in range(50000):
        candidates = [i for i in range(1, 100) if i not in used]
        attempt = random.sample(candidates, 12)
        square = [dob, attempt[0:4], attempt[4:8], attempt[8:12]]

        rows_ok = all(sum(row) == target_sum for row in square)
        cols_ok = all(sum(square[r][c] for r in range(4)) == target_sum for c in range(4))
        diag1 = sum(square[i][i] for i in range(4))
        diag2 = sum(square[i][3 - i] for i in range(4))

        if rows_ok and cols_ok and diag1 == target_sum and diag2 == target_sum:
            return {"square": square}

    return {"error": "No valid square found"}
