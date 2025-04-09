import unittest
from utils import calculate_points
from models import Receipt, Item

class TestPointCalculation(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            {
                "description": "Case 7: High-stress test with many rules: round +50, multiple .25 +25, time in 2pm-4pm => +10, odd day => +6, 4 items => +10, item desc multiples-of-3 => ?. Retailer name with digits => additional points.",
                "receipt": {
                    "retailer": "Shop24",
                    "purchaseDate": "2022-03-15",
                    "purchaseTime": "15:01",
                    "items": [
                        {"shortDescription": "ABCABCABC", "price": "4.00"},
                        {"shortDescription": "Foo Bar",    "price": "1.25"},
                        {"shortDescription": "12PackCola", "price": "3.75"},
                        {"shortDescription": "LunchBox",   "price": "5.00"}
                    ],
                    "total": "20.00"
                },
                "expected_points": 108
            },
            {
                "description": "Case 8: Check multiple rules with 5 items, partial-dollar total, not multiple of .25, odd day, time before 2pm.",
                "receipt": {
                    "retailer": "Target",
                    "purchaseDate": "2022-01-01",
                    "purchaseTime": "13:01",
                    "items": [
                        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                        {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
                    ],
                    "total": "35.35"
                },
                "expected_points": 28
            },
            {
                "description": "Case 9: Similar to earlier round-dollar example but with M&M Corner Market as the retailer.",
                "receipt": {
                    "retailer": "M&M Corner Market",
                    "purchaseDate": "2022-03-20",
                    "purchaseTime": "14:33",
                    "items": [
                        {"shortDescription": "Gatorade", "price": "2.25"},
                        {"shortDescription": "Gatorade", "price": "2.25"},
                        {"shortDescription": "Gatorade", "price": "2.25"},
                        {"shortDescription": "Gatorade", "price": "2.25"}
                    ],
                    "total": "9.00"
                },
                "expected_points": 109
            },
            {
                "description": "Case 10: Target123 receipt with cheese and eggs, round total, 2 items, retailer name with digits.",
                "receipt": {
                    "retailer": "Target123",
                    "purchaseDate": "2022-03-19",
                    "purchaseTime": "13:59",
                    "items": [
                        {"shortDescription": "Cheese", "price": "1.50"},
                        {"shortDescription": "Eggs", "price": "2.50"}
                    ],
                    "total": "4.00"
                },
                "expected_points": 96
            },
            {
                "description": "Case 11: Cost&Co receipt with 3 items including milk and toy, time 3:59pm, total $6.75.",
                "receipt": {
                    "retailer": "Cost&Co",
                    "purchaseDate": "2022-04-04",
                    "purchaseTime": "15:59",
                    "items": [
                        {"shortDescription": "Toy", "price": "1.00"},
                        {"shortDescription": "Tshirt", "price": "3.00"},
                        {"shortDescription": "Milk", "price": "2.75"}
                    ],
                    "total": "6.75"
                },
                "expected_points": 48
            },
            {
                "description": "Case 12: Walmart receipt with 1 banana item, roundish total $10.10.",
                "receipt": {
                    "retailer": "Walmart",
                    "purchaseDate": "2023-05-15",
                    "purchaseTime": "09:45",
                    "items": [
                        {"shortDescription": "Bananas", "price": "1.10"}
                    ],
                    "total": "10.10"
                },
                "expected_points": 13
            },
            {
                "description": "Case 13: 7Eleven! receipt with 5 identical items, round total, time exactly 2pm.",
                "receipt": {
                    "retailer": "7Eleven!",
                    "purchaseDate": "2024-12-31",
                    "purchaseTime": "14:00",
                    "items": [
                        {"shortDescription": "AAA", "price": "2.00"},
                        {"shortDescription": "BBB", "price": "2.00"},
                        {"shortDescription": "CCC", "price": "2.00"},
                        {"shortDescription": "DDD", "price": "2.00"},
                        {"shortDescription": "EEE", "price": "2.00"}
                    ],
                    "total": "16.00"
                },
                "expected_points": 103
            }
        ]

    def convert_to_receipt(self, receipt_dict):
        """Convert dictionary to Receipt object."""
        items = [Item(**item) for item in receipt_dict["items"]]
        return Receipt(
            retailer=receipt_dict["retailer"],
            purchaseDate=receipt_dict["purchaseDate"],
            purchaseTime=receipt_dict["purchaseTime"],
            items=items,
            total=receipt_dict["total"]
        )

    def test_point_calculation(self):
        """Test point calculation for all test cases."""
        for test_case in self.test_cases:
            with self.subTest(name=test_case["description"]):
                receipt = self.convert_to_receipt(test_case["receipt"])
                points = calculate_points(receipt)
                self.assertEqual(
                    points,
                    test_case["expected_points"],
                    f"\n{test_case['description']}\nExpected {test_case['expected_points']} points\nGot {points} points"
                )

if __name__ == '__main__':
    unittest.main()
