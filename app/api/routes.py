from fastapi import APIRouter, HTTPException, status
from app.api.models import (
    OptimizationInput,
    OptimizationResult,
    HealthResponse,
    ErrorResponse
)
from app.services.allocation_service import AllocationService
from app.core.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring and deployment verification.
    """
    return HealthResponse(
        status="healthy",
        version=settings.api_version,
        environment=settings.environment
    )


@router.post(
    "/optimize",
    response_model=OptimizationResult,
    status_code=status.HTTP_200_OK,
    tags=["Optimization"],
    summary="Optimize cargo allocation",
    description="""
    Optimize the allocation of cargos to tanks using a greedy First Fit Decreasing algorithm.
    
    **Algorithm:**
    - Sorts cargos by volume (descending) for better space utilization
    - Allocates each cargo to tanks with the most remaining capacity
    - Supports cargo splitting across multiple tanks
    - Ensures each tank only contains cargo from a single cargo ID
    
    **Constraints:**
    - All volumes and capacities must be positive numbers
    - Cargo IDs must be unique
    - Tank IDs must be unique
    - Each tank can only hold cargo from one cargo ID
    - Cargo splitting is allowed
    """
)
async def optimize_allocation(input_data: OptimizationInput):
    """
    Execute cargo allocation optimization.
    
    Args:
        input_data: Cargo and tank data for optimization
        
    Returns:
        Optimization result with allocations, metrics, and tank details
        
    Raises:
        HTTPException: If validation fails or optimization error occurs
    """
    try:
        AllocationService.validate_input_constraints(
            input_data,
            settings.max_cargo_count,
            settings.max_tank_count
        )
        
        logger.info(f"Starting optimization with {len(input_data.cargos)} cargos and {len(input_data.tanks)} tanks")
        
        result = AllocationService.optimize_allocation(input_data)
        
        logger.info(f"Optimization completed: {result['metrics']['total_loaded_volume']} units loaded")
        
        return OptimizationResult(
            allocations=result['allocations'],
            metrics=result['metrics'],
            tank_details=result['tank_details'],
            unallocated_cargo=result['unallocated_cargo']
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Optimization error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during optimization"
        )


@router.post(
    "/optimize/sample",
    response_model=OptimizationResult,
    status_code=status.HTTP_200_OK,
    tags=["Optimization"],
    summary="Run optimization with sample data",
    description="Execute optimization using the sample cargo and tank data from the assignment"
)
async def optimize_sample_data():
    """
    Run optimization with predefined sample data from the assignment.
    Useful for testing and demonstration purposes.
    """
    sample_input = OptimizationInput(
        cargos=[
            {"id": "C1", "volume": 1234},
            {"id": "C2", "volume": 4352},
            {"id": "C3", "volume": 3321},
            {"id": "C4", "volume": 2456},
            {"id": "C5", "volume": 5123},
            {"id": "C6", "volume": 1879},
            {"id": "C7", "volume": 4987},
            {"id": "C8", "volume": 2050},
            {"id": "C9", "volume": 3678},
            {"id": "C10", "volume": 5432}
        ],
        tanks=[
            {"id": "T1", "capacity": 5000},
            {"id": "T2", "capacity": 3000},
            {"id": "T3", "capacity": 4500},
            {"id": "T4", "capacity": 6000},
            {"id": "T5", "capacity": 2500},
            {"id": "T6", "capacity": 3500},
            {"id": "T7", "capacity": 4000},
            {"id": "T8", "capacity": 5500},
            {"id": "T9", "capacity": 3200},
            {"id": "T10", "capacity": 2800}
        ]
    )
    
    return await optimize_allocation(sample_input)
