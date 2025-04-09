import re
from datetime import datetime
from math import ceil
from models import Receipt, PointsBreakdown
from typing import Tuple

def calculate_points(receipt: Receipt) -> Tuple[int, PointsBreakdown]:
    points = 0
    print(f"\nCalculating points for receipt from {receipt.retailer}")

    # Rule 1: One point for every alphanumeric character in the retailer name
    retailer_points = len(re.findall(r'[a-zA-Z0-9]', receipt.retailer))
    points += retailer_points
    print(f"Rule 1 - {retailer_points} points for retailer name having {retailer_points} alphanumeric characters")

    # Convert the total to a float once for reuse
    total = float(receipt.total)

    # Rule 2: 50 points if the total is a round dollar amount (no cents)
    round_dollar = 0
    if abs(total - round(total)) < 1e-9:  # i.e. effectively integer
        round_dollar = 50
        points += round_dollar
        print("Rule 2 - 50 points for round dollar amount")

    # Rule 3: 25 points if the total is a multiple of 0.25
    quarter_multiple = 0
    if abs((total * 100) % 25) < 1e-9:  # Multiply by 100 to deal with floats as integers
        quarter_multiple = 25
        points += quarter_multiple
        print("Rule 3 - 25 points for total being multiple of 0.25")

    # Rule 4: 5 points for every two items
    pairs = len(receipt.items) // 2
    item_pairs = pairs * 5
    points += item_pairs
    print(f"Rule 4 - {item_pairs} points for {pairs} pairs of items")

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer
    description_bonus = 0
    for item in receipt.items:
        desc = ' '.join(item.shortDescription.split())
        desc_length = len(desc)
        if desc_length > 0 and desc_length % 3 == 0:
            item_points = ceil(float(item.price) * 0.2)
            description_bonus += item_points
            points += item_points
            print(f"Rule 5 - {item_points} points for '{desc}' (length {desc_length})")

    # Rule 6: 6 points if the day in the purchase date is odd
    odd_day = 0
    purchase_date = datetime.strptime(receipt.purchaseDate, '%Y-%m-%d')
    if purchase_date.day % 2 == 1:
        odd_day = 6
        points += odd_day
        print(f"Rule 6 - 6 points for odd day ({purchase_date.day})")

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    afternoon_bonus = 0
    purchase_time = datetime.strptime(receipt.purchaseTime, '%H:%M').time()
    start_time = datetime.strptime('14:00', '%H:%M').time()
    end_time = datetime.strptime('16:00', '%H:%M').time()
    if start_time < purchase_time < end_time:
        afternoon_bonus = 10
        points += afternoon_bonus
        print("Rule 7 - 10 points for time between 2:00pm and 4:00pm")

    print(f"Total points: {points}")
    
    breakdown = PointsBreakdown(
        retailerPoints=retailer_points,
        itemPairs=item_pairs,
        descriptionBonus=description_bonus,
        oddDay=odd_day,
        roundDollar=round_dollar,
        quarterMultiple=quarter_multiple,
        afternoonBonus=afternoon_bonus,
        total=points
    )
    
    return points, breakdown
