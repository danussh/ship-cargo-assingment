from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.api.routes import router
from app.core.config import settings
import logging

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="ShipIQ Cargo Optimization Service",
    description="""
    Production-ready cargo allocation system that optimizes loading of cargos into vessel tanks.
    
    ## Features
    - **Greedy First Fit Decreasing Algorithm**: Efficient cargo-to-tank allocation
    - **Cargo Splitting**: Supports splitting cargo across multiple tanks
    - **Single Cargo Constraint**: Each tank holds cargo from only one cargo ID
    - **Comprehensive Metrics**: Detailed utilization and allocation statistics
    - **Input Validation**: Robust validation using Pydantic models
    
    ## Algorithm
    The service uses a greedy First Fit Decreasing (FFD) approach:
    1. Sort cargos by volume (descending)
    2. Sort tanks by capacity (descending)
    3. For each cargo, allocate to tanks with most remaining capacity
    4. Support cargo splitting when needed
    5. Maintain constraint: one cargo ID per tank
    
    **Time Complexity**: O(n*m) where n = number of cargos, m = number of tanks
    **Space Complexity**: O(m) for tracking tank states
    """,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=f"/api/{settings.api_version}")

# Mount static files for UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Redirect root to the UI."""
    return RedirectResponse(url="/static/index.html")

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting ShipIQ Cargo Optimization Service v{settings.api_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Max cargos: {settings.max_cargo_count}, Max tanks: {settings.max_tank_count}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down ShipIQ Cargo Optimization Service")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development"
    )
