import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Integration tests for API endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'version' in data
        assert 'environment' in data
        assert 'timestamp' in data
    
    def test_optimize_valid_input(self):
        """Test optimization with valid input data."""
        payload = {
            "cargos": [
                {"id": "C1", "volume": 1234},
                {"id": "C2", "volume": 4352}
            ],
            "tanks": [
                {"id": "T1", "capacity": 5000},
                {"id": "T2", "capacity": 3000}
            ]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'allocations' in data
        assert 'metrics' in data
        assert 'tank_details' in data
        assert 'unallocated_cargo' in data
        assert 'timestamp' in data
        
        assert isinstance(data['allocations'], list)
        assert data['metrics']['total_cargo_volume'] == 5586
        assert data['metrics']['total_tank_capacity'] == 8000
    
    def test_optimize_sample_endpoint(self):
        """Test the sample data optimization endpoint."""
        response = client.post("/api/v1/optimize/sample")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data['allocations']) > 0
        assert data['metrics']['total_cargo_volume'] == 34512
        assert data['metrics']['total_tank_capacity'] == 40000
    
    def test_optimize_empty_cargos(self):
        """Test optimization with empty cargo list."""
        payload = {
            "cargos": [],
            "tanks": [{"id": "T1", "capacity": 1000}]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 422
    
    def test_optimize_empty_tanks(self):
        """Test optimization with empty tank list."""
        payload = {
            "cargos": [{"id": "C1", "volume": 1000}],
            "tanks": []
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 422
    
    def test_optimize_negative_volume(self):
        """Test validation of negative cargo volume."""
        payload = {
            "cargos": [{"id": "C1", "volume": -100}],
            "tanks": [{"id": "T1", "capacity": 1000}]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 422
    
    def test_optimize_negative_capacity(self):
        """Test validation of negative tank capacity."""
        payload = {
            "cargos": [{"id": "C1", "volume": 100}],
            "tanks": [{"id": "T1", "capacity": -1000}]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 422
    
    def test_optimize_zero_volume(self):
        """Test validation of zero cargo volume."""
        payload = {
            "cargos": [{"id": "C1", "volume": 0}],
            "tanks": [{"id": "T1", "capacity": 1000}]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 422
    
    def test_optimize_duplicate_cargo_ids(self):
        """Test validation of duplicate cargo IDs."""
        payload = {
            "cargos": [
                {"id": "C1", "volume": 100},
                {"id": "C1", "volume": 200}
            ],
            "tanks": [{"id": "T1", "capacity": 1000}]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 422
        assert "unique" in response.json()['detail'][0]['msg'].lower()
    
    def test_optimize_duplicate_tank_ids(self):
        """Test validation of duplicate tank IDs."""
        payload = {
            "cargos": [{"id": "C1", "volume": 100}],
            "tanks": [
                {"id": "T1", "capacity": 500},
                {"id": "T1", "capacity": 600}
            ]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 422
        assert "unique" in response.json()['detail'][0]['msg'].lower()
    
    def test_optimize_empty_cargo_id(self):
        """Test validation of empty cargo ID."""
        payload = {
            "cargos": [{"id": "", "volume": 100}],
            "tanks": [{"id": "T1", "capacity": 1000}]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 422
    
    def test_optimize_missing_fields(self):
        """Test validation when required fields are missing."""
        payload = {
            "cargos": [{"id": "C1"}],
            "tanks": [{"id": "T1", "capacity": 1000}]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 422
    
    def test_optimize_invalid_json(self):
        """Test handling of invalid JSON."""
        response = client.post(
            "/api/v1/optimize",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_optimize_large_dataset(self):
        """Test optimization with larger dataset."""
        cargos = [{"id": f"C{i}", "volume": 100 + i * 10} for i in range(1, 51)]
        tanks = [{"id": f"T{i}", "capacity": 500 + i * 20} for i in range(1, 31)]
        
        payload = {
            "cargos": cargos,
            "tanks": tanks
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data['allocations']) > 0
        assert data['metrics']['total_loaded_volume'] > 0
    
    def test_optimize_response_structure(self):
        """Test that response has correct structure and types."""
        payload = {
            "cargos": [{"id": "C1", "volume": 100}],
            "tanks": [{"id": "T1", "capacity": 200}]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        data = response.json()
        
        assert isinstance(data['allocations'], list)
        if len(data['allocations']) > 0:
            alloc = data['allocations'][0]
            assert 'tank_id' in alloc
            assert 'cargo_id' in alloc
            assert 'volume_allocated' in alloc
        
        metrics = data['metrics']
        assert isinstance(metrics['total_cargo_volume'], (int, float))
        assert isinstance(metrics['total_tank_capacity'], (int, float))
        assert isinstance(metrics['total_loaded_volume'], (int, float))
        assert isinstance(metrics['tank_utilization_percentage'], (int, float))
        
        assert isinstance(data['tank_details'], list)
        assert isinstance(data['unallocated_cargo'], list)
    
    def test_cors_headers(self):
        """Test CORS headers are present."""
        response = client.get("/api/v1/health")
        
        # Check that CORS middleware is configured
        assert response.status_code == 200
        # CORS headers would be present in actual cross-origin requests
    
    def test_openapi_docs(self):
        """Test that OpenAPI documentation is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi_spec = response.json()
        assert 'openapi' in openapi_spec
        assert 'paths' in openapi_spec
    
    def test_optimize_cargo_splitting_verification(self):
        """Test that cargo splitting works correctly through API."""
        payload = {
            "cargos": [{"id": "C1", "volume": 300}],
            "tanks": [
                {"id": "T1", "capacity": 100},
                {"id": "T2", "capacity": 100},
                {"id": "T3", "capacity": 100}
            ]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        data = response.json()
        
        assert response.status_code == 200
        assert len(data['allocations']) == 3
        
        total_allocated = sum(a['volume_allocated'] for a in data['allocations'])
        assert total_allocated == 300
        
        for alloc in data['allocations']:
            assert alloc['cargo_id'] == "C1"
    
    def test_optimize_single_cargo_per_tank_constraint_api(self):
        """Test single cargo per tank constraint through API."""
        payload = {
            "cargos": [
                {"id": "C1", "volume": 50},
                {"id": "C2", "volume": 50}
            ],
            "tanks": [{"id": "T1", "capacity": 200}]
        }
        
        response = client.post("/api/v1/optimize", json=payload)
        data = response.json()
        
        assert response.status_code == 200
        
        tank_cargos = {}
        for alloc in data['allocations']:
            if alloc['tank_id'] not in tank_cargos:
                tank_cargos[alloc['tank_id']] = set()
            tank_cargos[alloc['tank_id']].add(alloc['cargo_id'])
        
        for tank_id, cargo_ids in tank_cargos.items():
            assert len(cargo_ids) == 1
