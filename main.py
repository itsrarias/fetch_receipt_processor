from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from models import Receipt, ReceiptResponse, PointsResponse, PointsBreakdown
from utils import calculate_points
from pydantic import ValidationError
import uuid
from typing import Dict, Tuple

app = FastAPI(title="Receipt Processor")

# In-memory storage - dictionary to store points and breakdown
points_store: Dict[str, Tuple[int, PointsBreakdown]] = {}

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
        
        # Calculate points and get breakdown
        points, breakdown = calculate_points(receipt)
        print(f"Calculated points: {points}")
        
        # Store points and breakdown
        points_store[receipt_id] = (points, breakdown)
        print(f"Stored points in memory. Current store: {points_store}")
        
        return ReceiptResponse(id=receipt_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/receipts/{id}/points")
async def get_points(id: str, debug: bool = False):
    print(f"\nRetrieving points for receipt {id}")
    print(f"Current points store: {points_store}")
    
    if id not in points_store:
        print(f"Receipt {id} not found in store")
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    points, breakdown = points_store[id]
    print(f"Found {points} points for receipt {id}")
    
    response = PointsResponse(points=points, breakdown=breakdown if debug else None)
    return JSONResponse(content=response.dict(exclude_none=True))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 