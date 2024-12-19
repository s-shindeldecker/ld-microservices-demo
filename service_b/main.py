from fastapi import FastAPI, HTTPException
import time
import json

app = FastAPI(title="Service B - Optimized Sorting")

def optimized_sort(arr):
    start_time = time.time()
    sorted_arr = sorted(arr)
    end_time = time.time()
    return sorted_arr, end_time - start_time

@app.post("/sort")
async def sort_array(data: dict):
    try:
        numbers = data.get("numbers", [])
        if not numbers:
            raise HTTPException(status_code=400, detail="No numbers provided")
        
        sorted_array, processing_time = optimized_sort(numbers.copy())
        
        return {
            "sorted_array": sorted_array,
            "processing_time": processing_time,
            "service": "B - Optimized Sort"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
