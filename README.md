# Receipt Processor

A simple web service that awards points based on receipt data.

---

## 🔌 Endpoints

The service provides two endpoints:

### `POST /receipts/process`

- Accepts JSON for a receipt.
- Returns a JSON object containing a unique id.

### `GET /receipts/{id}/points`

- Returns the points awarded to the receipt specified by the provided id.

⚠️ All data is stored **in memory** and will be lost on application restart.

---

## 📁 Table of Contents

- [Requirements](#requirements)  
- [Project Structure](#project-structure)  
- [Running Locally (Python)](#running-locally-python)  
- [Running via Docker](#running-via-docker)  
- [Endpoints & Testing](#endpoints--testing)  
  - [POST /receipts/process](#post-receiptsprocess)  
  - [GET /receiptsidpoints](#get-receiptsidpoints)  
- [FAQ](#faq)

---

## Requirements

- Python 3.9+ (for local setup)
- `pip` for Python dependencies
- Docker (optional, for containerized setup)

---

## Project Structure

```
├── main.py              # Entry point for the service  
├── requirements.txt     # Python dependencies  
├── Dockerfile           # Docker build instructions  
├── README.md            # This file  
└── ...
```

- `main.py`: The web service logic (Flask, FastAPI, etc.)
- `requirements.txt`: Required packages

---

## Running Locally (Python)

1. Clone or download the repository.

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:

   ```bash
   python main.py
   ```

   - Default port is likely `8080`. Check console output to confirm.

4. Test it's running:

   - Visit [http://localhost:8080/](http://localhost:8080/) or move to [Endpoints & Testing](#📬-endpoints--testing)

---

## Running via Docker

Prefer Docker?

1. Build the Docker image:

   ```bash
   docker build -t receipt-processor .
   ```

2. Run the container:

   ```bash
   docker run -p 8080:8080 receipt-processor
   ```

3. Visit [http://localhost:8080/](http://localhost:8080/) to verify it's working.

---

## Endpoints & Testing

### `POST /receipts/process`

- Accepts JSON describing a receipt.
- Returns a receipt `id`.

#### Sample JSON Body

```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    { "shortDescription": "Mountain Dew 12PK", "price": "6.49" },
    { "shortDescription": "Emils Cheese Pizza", "price": "12.25" },
    { "shortDescription": "Knorr Creamy Chicken", "price": "1.26" },
    { "shortDescription": "Doritos Nacho Cheese", "price": "3.35" },
    { "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00" }
  ],
  "total": "35.35"
}
```

#### Bash `curl` Example

```bash
curl -X POST "http://localhost:8080/receipts/process" \
     -H "Content-Type: application/json" \
     -d @sample-receipt.json
```

#### Sample Response

```json
{
  "id": "d721c131-1255-4aa3-bdc1-456fe519c34f"
}
```

---

### `GET /receipts/{id}/points`

Retrieves the points for the given receipt id.

#### Example Request

```bash
curl -X GET "http://localhost:8080/receipts/d721c131-1255-4aa3-bdc1-456fe519c34f/points"
```

#### Sample Response

```json
{
  "points": 28
}
```

---

## FAQ

**Q1: My PowerShell terminal doesn’t accept `-X` in curl?**  
A1: PowerShell aliases `curl` to `Invoke-WebRequest`. Use:

```powershell
Invoke-RestMethod -Uri "http://localhost:8080/receipts/<id>/points" -Method GET
```

Or use `curl.exe` directly.

---

**Q2: Will the data persist after I stop the app?**  
A2: No. The app uses in-memory storage. Restarting the app or container will clear the data.

---

**Q3: How do I confirm my scoring logic is correct?**  
Use the sample receipts:

- The **Target** receipt should return **28 points**
- The **M&M Corner Market** example should return **109 points**

If they match, your logic is solid.

---

