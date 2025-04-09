from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date, time, datetime
import re

class Item(BaseModel):
    shortDescription: str = Field(..., pattern=r'^[\w\s\-]+$')
    price: str = Field(..., pattern=r'^\d+\.\d{2}$')

    @validator('shortDescription')
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError('Description cannot be empty or just whitespace')
        return v.strip()

class Receipt(BaseModel):
    retailer: str = Field(..., pattern=r'^[\w\s\-&]+$')
    purchaseDate: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    purchaseTime: str = Field(..., pattern=r'^\d{2}:\d{2}$')
    items: List[Item] = Field(..., min_items=1)
    total: str = Field(..., pattern=r'^\d+\.\d{2}$')

    @validator('retailer')
    def validate_retailer(cls, v):
        if not v.strip():
            raise ValueError('Retailer cannot be empty or just whitespace')
        return v.strip()

    @validator('purchaseDate')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Invalid date format, must be YYYY-MM-DD')
        return v

    @validator('purchaseTime')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('Invalid time format, must be HH:MM in 24-hour format')
        return v

    @validator('total')
    def validate_total(cls, v):
        try:
            total = float(v)
            if total < 0:
                raise ValueError('Total cannot be negative')
        except ValueError:
            raise ValueError('Invalid total amount')
        return v

class ReceiptResponse(BaseModel):
    id: str

class PointsBreakdown(BaseModel):
    retailerPoints: int
    itemPairs: int
    descriptionBonus: int
    oddDay: int
    roundDollar: Optional[int] = 0
    quarterMultiple: Optional[int] = 0
    afternoonBonus: Optional[int] = 0
    total: int

class PointsResponse(BaseModel):
    points: int
    breakdown: Optional[PointsBreakdown] = None

    class Config:
        json_encoders = {
            datetime: str
        }
        exclude_none = True  # This will omit null fields from the JSON response