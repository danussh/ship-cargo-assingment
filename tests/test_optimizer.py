import pytest
from app.core.optimizer import CargoOptimizer, Cargo, Tank


class TestCargoOptimizer:
    """Unit tests for the core optimization algorithm."""
    
    def test_simple_allocation(self):
        """Test basic allocation with cargo fitting perfectly in tanks."""
        cargos = [Cargo(id="C1", volume=100)]
        tanks = [Tank(id="T1", capacity=100)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert len(result['allocations']) == 1
        assert result['allocations'][0]['tank_id'] == "T1"
        assert result['allocations'][0]['cargo_id'] == "C1"
        assert result['allocations'][0]['volume_allocated'] == 100
        assert result['metrics']['total_loaded_volume'] == 100
        assert result['metrics']['tank_utilization_percentage'] == 100.0
        assert len(result['unallocated_cargo']) == 0
    
    def test_cargo_splitting(self):
        """Test cargo splitting across multiple tanks."""
        cargos = [Cargo(id="C1", volume=150)]
        tanks = [
            Tank(id="T1", capacity=100),
            Tank(id="T2", capacity=60)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert len(result['allocations']) == 2
        assert result['metrics']['total_loaded_volume'] == 150
        assert len(result['unallocated_cargo']) == 0
        
        allocations_by_tank = {a['tank_id']: a for a in result['allocations']}
        assert allocations_by_tank['T1']['volume_allocated'] == 100
        assert allocations_by_tank['T2']['volume_allocated'] == 50
    
    def test_single_cargo_per_tank_constraint(self):
        """Test that each tank only holds cargo from one cargo ID."""
        cargos = [
            Cargo(id="C1", volume=50),
            Cargo(id="C2", volume=30)
        ]
        tanks = [Tank(id="T1", capacity=100)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        tank_cargos = {}
        for alloc in result['allocations']:
            if alloc['tank_id'] not in tank_cargos:
                tank_cargos[alloc['tank_id']] = set()
            tank_cargos[alloc['tank_id']].add(alloc['cargo_id'])
        
        for tank_id, cargo_ids in tank_cargos.items():
            assert len(cargo_ids) == 1, f"Tank {tank_id} contains multiple cargo IDs: {cargo_ids}"
    
    def test_greedy_ordering(self):
        """Test that larger cargos are allocated first (greedy strategy)."""
        cargos = [
            Cargo(id="C1", volume=100),
            Cargo(id="C2", volume=200),
            Cargo(id="C3", volume=150)
        ]
        tanks = [
            Tank(id="T1", capacity=250),
            Tank(id="T2", capacity=200)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        # Greedy sorts: C2(200), C3(150), C1(100)
        # C2 goes to T1, C3 goes to T2, C1 can't fit (both tanks occupied)
        assert result['metrics']['total_loaded_volume'] == 350
        
        tank_details = {t['tank_id']: t for t in result['tank_details']}
        assert tank_details['T1']['cargo_id'] == "C2"
        assert tank_details['T2']['cargo_id'] == "C3"
    
    def test_unallocated_cargo(self):
        """Test handling of cargo that cannot be fully allocated."""
        cargos = [Cargo(id="C1", volume=500)]
        tanks = [Tank(id="T1", capacity=100)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert len(result['unallocated_cargo']) == 1
        assert result['unallocated_cargo'][0]['cargo_id'] == "C1"
        assert result['unallocated_cargo'][0]['unallocated_volume'] == 400
        assert result['metrics']['total_loaded_volume'] == 100
    
    def test_empty_inputs(self):
        """Test handling of empty cargo or tank lists."""
        optimizer = CargoOptimizer([], [])
        result = optimizer.optimize()
        
        assert len(result['allocations']) == 0
        assert result['metrics']['total_loaded_volume'] == 0
        assert result['metrics']['total_cargo_volume'] == 0
    
    def test_multiple_cargos_multiple_tanks(self):
        """Test complex scenario with multiple cargos and tanks."""
        cargos = [
            Cargo(id="C1", volume=1234),
            Cargo(id="C2", volume=4352),
            Cargo(id="C3", volume=3321)
        ]
        tanks = [
            Tank(id="T1", capacity=5000),
            Tank(id="T2", capacity=3000),
            Tank(id="T3", capacity=2000)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_cargo_volume'] == 8907
        assert result['metrics']['total_tank_capacity'] == 10000
        # Greedy sorts: C2(4352), C3(3321), C1(1234)
        # C2 goes to T1, C3 goes to T2, C1 can't fully fit in T3 (only 2000 capacity)
        # So only C2(4352) + C3(3000 of 3321) + C1(1234 won't fit) = 7352 or similar
        assert result['metrics']['total_loaded_volume'] >= 7000
        assert result['metrics']['total_loaded_volume'] <= 8000
    
    def test_assignment_sample_data(self):
        """Test with the exact sample data from the assignment."""
        cargos = [
            Cargo(id="C1", volume=1234),
            Cargo(id="C2", volume=4352),
            Cargo(id="C3", volume=3321),
            Cargo(id="C4", volume=2456),
            Cargo(id="C5", volume=5123),
            Cargo(id="C6", volume=1879),
            Cargo(id="C7", volume=4987),
            Cargo(id="C8", volume=2050),
            Cargo(id="C9", volume=3678),
            Cargo(id="C10", volume=5432)
        ]
        tanks = [
            Tank(id="T1", capacity=5000),
            Tank(id="T2", capacity=3000),
            Tank(id="T3", capacity=4500),
            Tank(id="T4", capacity=6000),
            Tank(id="T5", capacity=2500),
            Tank(id="T6", capacity=3500),
            Tank(id="T7", capacity=4000),
            Tank(id="T8", capacity=5500),
            Tank(id="T9", capacity=3200),
            Tank(id="T10", capacity=2800)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        total_cargo_volume = sum(c.volume for c in cargos)
        total_tank_capacity = sum(t.capacity for t in tanks)
        
        assert result['metrics']['total_cargo_volume'] == total_cargo_volume
        assert result['metrics']['total_tank_capacity'] == total_tank_capacity
        assert result['metrics']['total_loaded_volume'] <= total_tank_capacity
        assert result['metrics']['total_loaded_volume'] <= total_cargo_volume
        
        for tank_detail in result['tank_details']:
            if tank_detail['cargo_id'] is not None:
                cargo_allocations = [
                    a for a in result['allocations'] 
                    if a['tank_id'] == tank_detail['tank_id']
                ]
                assert all(a['cargo_id'] == tank_detail['cargo_id'] for a in cargo_allocations)
    
    def test_tank_utilization_metrics(self):
        """Test that tank utilization metrics are calculated correctly."""
        cargos = [Cargo(id="C1", volume=75)]
        tanks = [Tank(id="T1", capacity=100)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['tank_utilization_percentage'] == 75.0
        assert result['tank_details'][0]['utilization_percentage'] == 75.0
        assert result['tank_details'][0]['remaining_capacity'] == 25.0
    
    def test_zero_capacity_tank(self):
        """Test handling of tanks with zero capacity."""
        cargos = [Cargo(id="C1", volume=100)]
        tanks = [
            Tank(id="T1", capacity=0),
            Tank(id="T2", capacity=100)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 100
        tank_details = {t['tank_id']: t for t in result['tank_details']}
        assert tank_details['T1']['allocated_volume'] == 0
        assert tank_details['T2']['allocated_volume'] == 100
    
    def test_all_tanks_smaller_than_cargo(self):
        """Test when all tanks are smaller than the smallest cargo."""
        cargos = [Cargo(id="C1", volume=1000)]
        tanks = [
            Tank(id="T1", capacity=100),
            Tank(id="T2", capacity=200),
            Tank(id="T3", capacity=150)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 450
        assert len(result['unallocated_cargo']) == 1
        assert result['unallocated_cargo'][0]['unallocated_volume'] == 550
    
    def test_metrics_consistency(self):
        """Test that all metrics are consistent with allocations."""
        cargos = [
            Cargo(id="C1", volume=100),
            Cargo(id="C2", volume=200)
        ]
        tanks = [
            Tank(id="T1", capacity=150),
            Tank(id="T2", capacity=200)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        total_allocated = sum(a['volume_allocated'] for a in result['allocations'])
        assert total_allocated == result['metrics']['total_loaded_volume']
        
        total_unallocated = sum(u['unallocated_volume'] for u in result['unallocated_cargo'])
        assert total_unallocated == result['metrics']['total_unallocated_volume']
        
        assert (result['metrics']['total_loaded_volume'] + 
                result['metrics']['total_unallocated_volume'] == 
                result['metrics']['total_cargo_volume'])
