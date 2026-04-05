from typing import Dict
from app.core.optimizer import CargoOptimizer, Cargo, Tank
from app.api.models import OptimizationInput, OptimizationResult


class AllocationService:
    """
    Service layer for cargo allocation operations.
    Handles business logic and orchestrates the optimization process.
    """
    
    @staticmethod
    def optimize_allocation(input_data: OptimizationInput) -> Dict:
        """
        Execute cargo allocation optimization.
        
        Args:
            input_data: Validated input containing cargos and tanks
            
        Returns:
            Optimization result with allocations and metrics
        """
        cargos = [
            Cargo(id=cargo.id, volume=cargo.volume)
            for cargo in input_data.cargos
        ]
        
        tanks = [
            Tank(id=tank.id, capacity=tank.capacity)
            for tank in input_data.tanks
        ]
        
        optimizer = CargoOptimizer(cargos=cargos, tanks=tanks)
        result = optimizer.optimize()
        
        return result
    
    @staticmethod
    def validate_input_constraints(input_data: OptimizationInput, max_cargo: int, max_tank: int) -> None:
        """
        Validate input against system constraints.
        
        Args:
            input_data: Input to validate
            max_cargo: Maximum allowed cargo count
            max_tank: Maximum allowed tank count
            
        Raises:
            ValueError: If constraints are violated
        """
        if len(input_data.cargos) > max_cargo:
            raise ValueError(f"Number of cargos ({len(input_data.cargos)}) exceeds maximum allowed ({max_cargo})")
        
        if len(input_data.tanks) > max_tank:
            raise ValueError(f"Number of tanks ({len(input_data.tanks)}) exceeds maximum allowed ({max_tank})")
