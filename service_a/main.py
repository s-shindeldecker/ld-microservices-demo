from fastapi import FastAPI, HTTPException
import time
import json

app = FastAPI(title="Service A - Basic Sorting")

def bubble_sort(arr):
    n = len(arr)
    start_time = time.time()
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    end_time = time.time()
    return arr, end_time - start_time

@app.post("/sort")
async def sort_array(data: dict):
    try:
        numbers = data.get("numbers", [])
        if not numbers:
            raise HTTPException(status_code=400, detail="No numbers provided")
        
        sorted_array, processing_time = bubble_sort(numbers.copy())
        
        return {
            "sorted_array": sorted_array,
            "processing_time": processing_time,
            "service": "A - Bubble Sort"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
