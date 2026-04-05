from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class CargoInput(BaseModel):
    id: str = Field(..., description="Unique identifier for the cargo")
    volume: float = Field(..., gt=0, description="Volume of the cargo in cubic units")
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Cargo ID cannot be empty")
        return v.strip()


class TankInput(BaseModel):
    id: str = Field(..., description="Unique identifier for the tank")
    capacity: float = Field(..., gt=0, description="Capacity of the tank in cubic units")
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Tank ID cannot be empty")
        return v.strip()


class OptimizationInput(BaseModel):
    cargos: List[CargoInput] = Field(..., min_length=1, description="List of cargos to allocate")
    tanks: List[TankInput] = Field(..., min_length=1, description="List of available tanks")
    
    @field_validator('cargos')
    @classmethod
    def validate_unique_cargo_ids(cls, v: List[CargoInput]) -> List[CargoInput]:
        ids = [cargo.id for cargo in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Cargo IDs must be unique")
        return v
    
    @field_validator('tanks')
    @classmethod
    def validate_unique_tank_ids(cls, v: List[TankInput]) -> List[TankInput]:
        ids = [tank.id for tank in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Tank IDs must be unique")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "cargos": [
                    {"id": "C1", "volume": 1234},
                    {"id": "C2", "volume": 4352},
                    {"id": "C3", "volume": 3321}
                ],
                "tanks": [
                    {"id": "T1", "volume": 5000},
                    {"id": "T2", "volume": 3000},
                    {"id": "T3", "volume": 2000}
                ]
            }
        }


class AllocationDetail(BaseModel):
    tank_id: str
    cargo_id: str
    volume_allocated: float


class OptimizationMetrics(BaseModel):
    total_cargo_volume: float
    total_tank_capacity: float
    total_loaded_volume: float
    total_unallocated_volume: float
    tank_utilization_percentage: float
    cargo_loaded_percentage: float
    number_of_allocations: int
    tanks_used: int
    tanks_total: int


class TankDetail(BaseModel):
    tank_id: str
    capacity: float
    allocated_volume: float
    remaining_capacity: float
    cargo_id: Optional[str]
    utilization_percentage: float


class UnallocatedCargo(BaseModel):
    cargo_id: str
    unallocated_volume: float
    original_volume: float


class OptimizationResult(BaseModel):
    allocations: List[AllocationDetail]
    metrics: OptimizationMetrics
    tank_details: List[TankDetail]
    unallocated_cargo: List[UnallocatedCargo]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "allocations": [
                    {"tank_id": "T1", "cargo_id": "C2", "volume_allocated": 4352},
                    {"tank_id": "T2", "cargo_id": "C3", "volume_allocated": 3000}
                ],
                "metrics": {
                    "total_cargo_volume": 8907,
                    "total_tank_capacity": 10000,
                    "total_loaded_volume": 7352,
                    "total_unallocated_volume": 1555,
                    "tank_utilization_percentage": 73.52,
                    "cargo_loaded_percentage": 82.54,
                    "number_of_allocations": 2,
                    "tanks_used": 2,
                    "tanks_total": 3
                },
                "tank_details": [],
                "unallocated_cargo": [],
                "timestamp": "2026-04-05T08:17:00.000Z"
            }
        }


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
