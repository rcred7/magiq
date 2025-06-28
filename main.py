from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import itertools

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FirstRow(BaseModel):
    row: List[int]

@app.post("/generate")
def generate_magic_square(data: FirstRow):
    first_row = data.row
    if len(first_row) != 4 or any(not (1 <= x < 100) for x in first_row):
        return {"error": "Input must be 4 integers between 1 and 99"}

    magic_sum = sum(first_row)
    used = set(first_row)

    # Step 1: Get all candidates for remaining values
    available = [i for i in range(1, 100) if i not in used]

    # Step 2: Backtracking
    def is_valid(grid):
        # Rows
        for row in grid:
            if sum(row) != magic_sum:
                return False
        # Columns
        for c in range(4):
            if sum(grid[r][c] for r in range(4)) != magic_sum:
                return False
        # Diagonals
        if sum(grid[i][i] for i in range(4)) != magic_sum:
            return False
        if sum(grid[i][3 - i] for i in range(4)) != magic_sum:
            return False
        return True

    def backtrack(path: List[int], depth: int) -> Optional[List[List[int]]]:
        if len(path) == 12:
            grid = [
                first_row,
                path[0:4],
                path[4:8],
                path[8:12]
            ]
            if is_valid(grid):
                return grid
            return None

        for val in available:
            if val in path:
                continue
            res = backtrack(path + [val], depth + 1)
            if res:
                return res
        return None

    solution = backtrack([], 0)
    if solution:
        return {"square": solution}
    else:
        return {"error": "No valid square found"}
