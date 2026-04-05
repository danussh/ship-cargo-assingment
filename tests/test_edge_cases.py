import pytest
from app.core.optimizer import CargoOptimizer, Cargo, Tank


class TestEdgeCases:
    """Edge case tests for cargo optimization."""
    
    def test_single_cargo_single_tank_exact_fit(self):
        """Test perfect fit scenario."""
        cargos = [Cargo(id="C1", volume=1000)]
        tanks = [Tank(id="T1", capacity=1000)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 1000
        assert result['metrics']['tank_utilization_percentage'] == 100.0
        assert len(result['unallocated_cargo']) == 0
    
    def test_very_small_volumes(self):
        """Test with very small decimal volumes."""
        cargos = [Cargo(id="C1", volume=0.001)]
        tanks = [Tank(id="T1", capacity=0.002)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 0.001
        assert len(result['unallocated_cargo']) == 0
    
    def test_very_large_volumes(self):
        """Test with very large volumes."""
        cargos = [Cargo(id="C1", volume=1000000)]
        tanks = [Tank(id="T1", capacity=2000000)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 1000000
        assert len(result['unallocated_cargo']) == 0
    
    def test_many_small_cargos_few_large_tanks(self):
        """Test many small cargos with few large tanks."""
        cargos = [Cargo(id=f"C{i}", volume=10) for i in range(100)]
        tanks = [Tank(id="T1", capacity=500), Tank(id="T2", capacity=500)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        # With single cargo per tank constraint, only 2 cargos can be loaded (one per tank)
        assert result['metrics']['total_loaded_volume'] == 20
        assert result['metrics']['total_cargo_volume'] == 1000
        assert len(result['unallocated_cargo']) == 98
    
    def test_many_large_cargos_many_small_tanks(self):
        """Test many large cargos with many small tanks."""
        cargos = [Cargo(id=f"C{i}", volume=1000) for i in range(10)]
        tanks = [Tank(id=f"T{i}", capacity=100) for i in range(50)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 5000
        assert result['metrics']['total_unallocated_volume'] == 5000
    
    def test_all_cargos_larger_than_all_tanks(self):
        """Test when every cargo is larger than every tank."""
        cargos = [
            Cargo(id="C1", volume=1000),
            Cargo(id="C2", volume=2000),
            Cargo(id="C3", volume=1500)
        ]
        tanks = [
            Tank(id="T1", capacity=500),
            Tank(id="T2", capacity=400),
            Tank(id="T3", capacity=300)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 1200
        assert len(result['unallocated_cargo']) == 3
    
    def test_one_huge_cargo_many_tiny_tanks(self):
        """Test one huge cargo split across many tiny tanks."""
        cargos = [Cargo(id="C1", volume=1000)]
        tanks = [Tank(id=f"T{i}", capacity=10) for i in range(100)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 1000
        assert len(result['allocations']) == 100
        assert all(a['cargo_id'] == "C1" for a in result['allocations'])
    
    def test_identical_volumes_and_capacities(self):
        """Test when all cargos and tanks have identical values."""
        cargos = [Cargo(id=f"C{i}", volume=100) for i in range(5)]
        tanks = [Tank(id=f"T{i}", capacity=100) for i in range(5)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 500
        assert len(result['unallocated_cargo']) == 0
    
    def test_fractional_allocations(self):
        """Test that fractional allocations work correctly."""
        cargos = [Cargo(id="C1", volume=123.456)]
        tanks = [
            Tank(id="T1", capacity=100.5),
            Tank(id="T2", capacity=50.0)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert abs(result['metrics']['total_loaded_volume'] - 123.456) < 0.001
    
    def test_single_tank_multiple_splits_same_cargo(self):
        """Test that a cargo can be split and allocated to same tank multiple times is prevented."""
        cargos = [Cargo(id="C1", volume=200)]
        tanks = [Tank(id="T1", capacity=300)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        tank_allocations = [a for a in result['allocations'] if a['tank_id'] == "T1"]
        assert len(tank_allocations) == 1
        assert tank_allocations[0]['volume_allocated'] == 200
    
    def test_optimal_packing_order(self):
        """Test that greedy approach provides reasonable packing."""
        cargos = [
            Cargo(id="C1", volume=5000),
            Cargo(id="C2", volume=3000),
            Cargo(id="C3", volume=2000)
        ]
        tanks = [
            Tank(id="T1", capacity=6000),
            Tank(id="T2", capacity=4000)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        # C1 (5000) goes to T1, C2 (3000) goes to T2
        # C3 (2000) can't fit because both tanks are occupied
        assert result['metrics']['total_loaded_volume'] == 8000
        assert len(result['unallocated_cargo']) == 1
    
    def test_no_waste_when_possible(self):
        """Test that algorithm minimizes waste when perfect allocation exists."""
        cargos = [
            Cargo(id="C1", volume=100),
            Cargo(id="C2", volume=200),
            Cargo(id="C3", volume=300)
        ]
        tanks = [
            Tank(id="T1", capacity=100),
            Tank(id="T2", capacity=200),
            Tank(id="T3", capacity=300)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 600
        assert result['metrics']['tank_utilization_percentage'] == 100.0
    
    def test_partial_allocation_metrics(self):
        """Test metrics when only partial allocation is possible."""
        cargos = [Cargo(id="C1", volume=1000)]
        tanks = [Tank(id="T1", capacity=300)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['cargo_loaded_percentage'] == 30.0
        assert result['metrics']['tank_utilization_percentage'] == 100.0
    
    def test_multiple_tanks_same_capacity(self):
        """Test allocation when multiple tanks have same capacity."""
        cargos = [Cargo(id="C1", volume=500)]
        tanks = [
            Tank(id="T1", capacity=200),
            Tank(id="T2", capacity=200),
            Tank(id="T3", capacity=200)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] == 500
        
        c1_allocations = [a for a in result['allocations'] if a['cargo_id'] == "C1"]
        assert len(c1_allocations) <= 3
    
    def test_rounding_precision(self):
        """Test that rounding doesn't cause issues."""
        cargos = [Cargo(id="C1", volume=1.0/3.0)]
        tanks = [Tank(id="T1", capacity=1.0)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] > 0
        assert len(result['unallocated_cargo']) == 0
    
    def test_stress_test_large_scale(self):
        """Stress test with large number of cargos and tanks."""
        cargos = [Cargo(id=f"C{i}", volume=100 + i) for i in range(1000)]
        tanks = [Tank(id=f"T{i}", capacity=200 + i) for i in range(500)]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        assert result['metrics']['total_loaded_volume'] > 0
        assert isinstance(result['allocations'], list)
        assert isinstance(result['metrics'], dict)
    
    def test_alternating_sizes(self):
        """Test with alternating large and small cargos."""
        cargos = [
            Cargo(id="C1", volume=1000),
            Cargo(id="C2", volume=100),
            Cargo(id="C3", volume=1000),
            Cargo(id="C4", volume=100)
        ]
        tanks = [
            Tank(id="T1", capacity=1100),
            Tank(id="T2", capacity=1100)
        ]
        
        optimizer = CargoOptimizer(cargos, tanks)
        result = optimizer.optimize()
        
        # Greedy sorts by volume: C1(1000), C3(1000), C2(100), C4(100)
        # C1 goes to T1, C3 goes to T2, C2 and C4 can't fit (tanks occupied)
        assert result['metrics']['total_loaded_volume'] == 2000
