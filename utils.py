import re
from datetime import datetime
from math import ceil
from models import Receipt

def calculate_points(receipt: Receipt) -> int:
    points = 0
    print(f"\nCalculating points for receipt from {receipt.retailer}")

    # Rule 1: One point for every alphanumeric character in the retailer name
    alphanumeric_chars = len(re.findall(r'[a-zA-Z0-9]', receipt.retailer))
    points += alphanumeric_chars
    print(f"Rule 1 - {alphanumeric_chars} points for retailer name having {alphanumeric_chars} alphanumeric characters")

    # Convert the total to a float once for reuse
    total = float(receipt.total)

    # Rule 2: 50 points if the total is a round dollar amount (no cents)
    # Use total.is_integer() carefully; if totals are not exact floats,
    # consider a small epsilon or integer check.
    if abs(total - round(total)) < 1e-9:  # i.e. effectively integer
        points += 50
        print("Rule 2 - 50 points for round dollar amount")

    # Rule 3: 25 points if the total is a multiple of 0.25
    if abs((total * 100) % 25) < 1e-9:  # Multiply by 100 to deal with floats as integers
        points += 25
        print("Rule 3 - 25 points for total being multiple of 0.25")

    # Rule 4: 5 points for every two items
    pairs = len(receipt.items) // 2
    pair_points = pairs * 5
    points += pair_points
    print(f"Rule 4 - {pair_points} points for {pairs} pairs of items")

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer
    for item in receipt.items:
        desc = ' '.join(item.shortDescription.split())
        desc_length = len(desc)
        if desc_length > 0 and desc_length % 3 == 0:
            item_points = ceil(float(item.price) * 0.2)
            points += item_points
            print(f"Rule 5 - {item_points} points for '{desc}' (length {desc_length})")

    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(receipt.purchaseDate, '%Y-%m-%d')
    if purchase_date.day % 2 == 1:
        points += 6
        print(f"Rule 6 - 6 points for odd day ({purchase_date.day})")

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt.purchaseTime, '%H:%M').time()
    start_time = datetime.strptime('14:00', '%H:%M').time()
    end_time = datetime.strptime('16:00', '%H:%M').time()
    if start_time < purchase_time < end_time:
        points += 10
        print("Rule 7 - 10 points for time between 2:00pm and 4:00pm")

    print(f"Total points: {points}")
    return points
