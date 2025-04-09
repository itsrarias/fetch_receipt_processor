from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from models import Receipt, ReceiptResponse, PointsResponse
from utils import calculate_points
from pydantic import ValidationError
import uuid
from typing import Dict

app = FastAPI(title="Receipt Processor")

# In-memory storage - dictionary to store points
points_store: Dict[str, int] = {}

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.post("/receipts/process", response_model=ReceiptResponse)
async def process_receipt(receipt: Receipt):
    try:
        print("\nProcessing new receipt...")
        
        # Generate a real UUID
        receipt_id = str(uuid.uuid4())
        print(f"Generated ID: {receipt_id}")
        
        # Calculate points
        points = calculate_points(receipt)
        print(f"Calculated points: {points}")
        
        # Store points
        points_store[receipt_id] = points
        print(f"Stored points in memory. Current store: {points_store}")
        
        return ReceiptResponse(id=receipt_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/receipts/{id}/points", response_model=PointsResponse)
async def get_points(id: str):
    print(f"\nRetrieving points for receipt {id}")
    print(f"Current points store: {points_store}")
    
    # Check if receipt exists in store
    if id not in points_store:
        print(f"Receipt {id} not found in store")
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    points = points_store[id]
    print(f"Found {points} points for receipt {id}")
    return PointsResponse(points=points)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 