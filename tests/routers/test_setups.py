import pytest


class TestSetupsRouter:
    """Tests for setups API endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_setup(self, client, sample_setup_data):
        """Test creating a new setup."""
        response = await client.post("/api/v1/setups/", json=sample_setup_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_setup_data["name"]
        assert data["notes"] == sample_setup_data["notes"]
        assert "_id" in data
        assert "user_id" in data
    
    @pytest.mark.asyncio
    async def test_create_setup_without_notes(self, client):
        """Test creating a setup without notes."""
        setup_data = {"name": "Simple Strategy"}
        response = await client.post("/api/v1/setups/", json=setup_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Simple Strategy"
        assert data["notes"] is None
    
    @pytest.mark.asyncio
    async def test_create_setup_missing_name(self, client):
        """Test creating setup without name fails."""
        setup_data = {"notes": "Some notes without a name"}
        response = await client.post("/api/v1/setups/", json=setup_data)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_get_all_setups(self, client, sample_setup_data):
        """Test getting all setups."""
        # Create a few setups
        await client.post("/api/v1/setups/", json=sample_setup_data)
        await client.post("/api/v1/setups/", json={
            "name": "Another Strategy",
            "notes": "Different approach"
        })
        
        # Get all setups
        response = await client.get("/api/v1/setups/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
        
        # Verify all setups have required fields
        for setup in data:
            assert "name" in setup
            assert "_id" in setup
            assert "user_id" in setup
    
    @pytest.mark.asyncio
    async def test_get_setups_empty(self, client):
        """Test getting setups when none exist."""
        response = await client.get("/api/v1/setups/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
