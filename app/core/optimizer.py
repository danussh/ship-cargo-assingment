from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Cargo:
    id: str
    volume: float


@dataclass
class Tank:
    id: str
    capacity: float


@dataclass
class Allocation:
    tank_id: str
    cargo_id: str
    volume_allocated: float


class CargoOptimizer:
    """
    Greedy cargo allocation optimizer using First Fit Decreasing (FFD) strategy.
    
    Algorithm:
    1. Sort cargos by volume (descending) - larger items first for better packing
    2. Sort tanks by capacity (descending) - prioritize larger tanks
    3. For each cargo, allocate to tanks with most remaining capacity
    4. Support cargo splitting across multiple tanks
    5. Constraint: Each tank can only hold cargo from a single cargo ID
    
    Time Complexity: O(n*m) where n=cargos, m=tanks
    Space Complexity: O(m) for tracking tank states
    """
    
    def __init__(self, cargos: List[Cargo], tanks: List[Tank]):
        self.cargos = cargos
        self.tanks = tanks
        self.allocations: List[Allocation] = []
        self.tank_states: Dict[str, Dict] = {}
        
    def optimize(self) -> Dict:
        """
        Execute the optimization algorithm.
        
        Returns:
            Dictionary containing allocations, metrics, and unallocated cargo
        """
        self._initialize_tank_states()
        
        sorted_cargos = sorted(self.cargos, key=lambda c: c.volume, reverse=True)
        sorted_tanks = sorted(self.tanks, key=lambda t: t.capacity, reverse=True)
        
        unallocated_cargo = []
        
        for cargo in sorted_cargos:
            remaining_volume = cargo.volume
            
            available_tanks = self._get_available_tanks_for_cargo(cargo.id, sorted_tanks)
            
            for tank in available_tanks:
                if remaining_volume <= 0:
                    break
                    
                tank_state = self.tank_states[tank.id]
                available_capacity = tank_state['remaining_capacity']
                
                if available_capacity > 0:
                    volume_to_allocate = min(remaining_volume, available_capacity)
                    
                    self.allocations.append(Allocation(
                        tank_id=tank.id,
                        cargo_id=cargo.id,
                        volume_allocated=volume_to_allocate
                    ))
                    
                    tank_state['remaining_capacity'] -= volume_to_allocate
                    tank_state['cargo_id'] = cargo.id
                    tank_state['allocated_volume'] += volume_to_allocate
                    
                    remaining_volume -= volume_to_allocate
            
            if remaining_volume > 0:
                unallocated_cargo.append({
                    'cargo_id': cargo.id,
                    'unallocated_volume': remaining_volume,
                    'original_volume': cargo.volume
                })
        
        return self._generate_result(unallocated_cargo)
    
    def _initialize_tank_states(self):
        """Initialize tracking state for each tank."""
        for tank in self.tanks:
            self.tank_states[tank.id] = {
                'capacity': tank.capacity,
                'remaining_capacity': tank.capacity,
                'cargo_id': None,
                'allocated_volume': 0.0
            }
    
    def _get_available_tanks_for_cargo(self, cargo_id: str, sorted_tanks: List[Tank]) -> List[Tank]:
        """
        Get tanks available for a specific cargo.
        A tank is available if:
        1. It has remaining capacity AND
        2. Either it's empty OR it already contains this cargo
        """
        available = []
        for tank in sorted_tanks:
            state = self.tank_states[tank.id]
            if state['remaining_capacity'] > 0:
                if state['cargo_id'] is None or state['cargo_id'] == cargo_id:
                    available.append(tank)
        
        return sorted(available, key=lambda t: self.tank_states[t.id]['remaining_capacity'], reverse=True)
    
    def _generate_result(self, unallocated_cargo: List[Dict]) -> Dict:
        """Generate the final optimization result with metrics."""
        total_capacity = sum(tank.capacity for tank in self.tanks)
        total_loaded = sum(alloc.volume_allocated for alloc in self.allocations)
        total_cargo_volume = sum(cargo.volume for cargo in self.cargos)
        
        utilization_percentage = (total_loaded / total_capacity * 100) if total_capacity > 0 else 0
        cargo_loaded_percentage = (total_loaded / total_cargo_volume * 100) if total_cargo_volume > 0 else 0
        
        tank_utilization = []
        for tank in self.tanks:
            state = self.tank_states[tank.id]
            tank_util = (state['allocated_volume'] / state['capacity'] * 100) if state['capacity'] > 0 else 0
            tank_utilization.append({
                'tank_id': tank.id,
                'capacity': state['capacity'],
                'allocated_volume': state['allocated_volume'],
                'remaining_capacity': state['remaining_capacity'],
                'cargo_id': state['cargo_id'],
                'utilization_percentage': round(tank_util, 2)
            })
        
        return {
            'allocations': [
                {
                    'tank_id': alloc.tank_id,
                    'cargo_id': alloc.cargo_id,
                    'volume_allocated': alloc.volume_allocated
                }
                for alloc in self.allocations
            ],
            'metrics': {
                'total_cargo_volume': total_cargo_volume,
                'total_tank_capacity': total_capacity,
                'total_loaded_volume': total_loaded,
                'total_unallocated_volume': total_cargo_volume - total_loaded,
                'tank_utilization_percentage': round(utilization_percentage, 2),
                'cargo_loaded_percentage': round(cargo_loaded_percentage, 2),
                'number_of_allocations': len(self.allocations),
                'tanks_used': len([t for t in tank_utilization if t['allocated_volume'] > 0]),
                'tanks_total': len(self.tanks)
            },
            'tank_details': sorted(tank_utilization, key=lambda x: x['utilization_percentage'], reverse=True),
            'unallocated_cargo': unallocated_cargo
        }
