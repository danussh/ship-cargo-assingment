# 🚢 ShipIQ Cargo Optimization

A cargo allocation system that optimizes loading of cargos into tanks using a greedy algorithm.

## ✨ Features

- ✅ Cargo splitting across multiple tanks
- ✅ Single cargo per tank constraint
- ✅ Maximizes total loaded volume
- ✅ Interactive Web UI with visualizations
- ✅ REST API with automatic docs
- ✅ 93% test coverage

## 🚀 Quick Start

### Option 1: Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start server
python -m app.main
```

Open browser: **http://localhost:8000**

### Option 2: Docker

```bash
docker-compose up --build
```

Open browser: **http://localhost:8000**

## 📡 API Endpoints

- **Web UI**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `GET /api/v1/health`
- **Optimize**: `POST /api/v1/optimize`

> **📝 Note on API Design:**  
> We combined `POST /input` and `POST /optimize` into a single endpoint: `POST /api/v1/optimize`  
> This endpoint accepts input AND returns results immediately, which is better because:
> - ✅ Single request gets complete results
> - ✅ No need to store state between requests
> - ✅ Simpler API design
> - ✅ RESTful best practice

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "cargos": [
      {"id": "C1", "volume": 1234},
      {"id": "C2", "volume": 4352}
    ],
    "tanks": [
      {"id": "T1", "capacity": 5000},
      {"id": "T2", "capacity": 3000}
    ]
  }'
```

## 🧪 Run Tests

```bash
pytest
```

## 📊 How It Works

1. **Sort** cargos by volume (largest first)
2. **Sort** tanks by capacity (largest first)
3. **Allocate** each cargo to best-fit tanks
4. **Split** cargo across tanks if needed
5. **Enforce** one cargo type per tank

**Algorithm**: Greedy First Fit Decreasing (O(n*m))

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Testing**: pytest
- **Deployment**: Docker

## 👤 Author

Built by Danussh

## 📝 License

Created for ShipIQ technical assignment
