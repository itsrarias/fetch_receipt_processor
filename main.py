from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from models import Receipt, ReceiptResponse, PointsResponse, PointsBreakdown
from utils import calculate_points
from pydantic import ValidationError
import uuid
from typing import Dict, Tuple

# Create FastAPI app instance
app = FastAPI(title="Receipt Processor")

# In-memory storage to keep track of receipt points and their breakdowns
points_store: Dict[str, Tuple[int, PointsBreakdown]] = {}

# Handle validation errors from Pydantic (e.g., bad input data)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

# Endpoint to process a new receipt and assign points
@app.post("/receipts/process", response_model=ReceiptResponse)
async def process_receipt(receipt: Receipt):
    try:
        print("\nProcessing new receipt...")
        
        # Create a unique ID for this receipt
        receipt_id = str(uuid.uuid4())
        print(f"Generated ID: {receipt_id}")
        
        # Calculate points for the receipt using a custom utility function
        points, breakdown = calculate_points(receipt)
        print(f"Calculated points: {points}")
        
        # Save the result in memory
        points_store[receipt_id] = (points, breakdown)
        print(f"Stored points in memory. Current store: {points_store}")
        
        # Return the ID of the processed receipt
        return ReceiptResponse(id=receipt_id)
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Endpoint to retrieve points (and optionally the breakdown) for a given receipt ID
@app.get("/receipts/{id}/points")
async def get_points(id: str, debug: bool = False):
    print(f"\nRetrieving points for receipt {id}")
    print(f"Current points store: {points_store}")
    
    # Check if receipt ID exists
    if id not in points_store:
        print(f"Receipt {id} not found in store")
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    # Get points and breakdown from memory
    points, breakdown = points_store[id]
    print(f"Found {points} points for receipt {id}")
    
    # If debug flag is true, include breakdown in response
    response = PointsResponse(points=points, breakdown=breakdown if debug else None)
    return JSONResponse(content=response.dict(exclude_none=True))

# Optional: run the app directly with Uvicorn if this file is executed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
