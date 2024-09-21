import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test login success
def test_login_success():
    response = client.post(
        "/token",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test login failure
def test_login_invalid_credentials():
    response = client.post(
        "/token",
        json={"username": "wronguser", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

# Mocking external API call for fetching mutual funds
@patch("app.mutual_funds.httpx.AsyncClient")
async def test_fetch_funds_success(mock_client):
    mock_instance = AsyncMock()
    mock_client.return_value = mock_instance

    # Setup the mock response
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value=[
        {
            "Scheme_Code": 133366,
            "ISIN_Div_Payout_ISIN_Growth": "INF179KA1Q38",
            "ISIN_Div_Reinvestment": "-",
            "Scheme_Name": "HDFC Income Fund - Normal IDCW Option",
            "Net_Asset_Value": 17.3884,
            "Date": "20-Sep-2024",
            "Scheme_Type": "Open Ended Schemes",
            "Scheme_Category": "Debt Scheme - Medium to Long Duration Fund",
            "Mutual_Fund_Family": "HDFC Mutual Fund"
        }
    ])
    
    # Ensure that the __aenter__ method of the AsyncMock instance returns the mock response
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.get.return_value = mock_response

    response = client.get(
        "/funds/HDFC Mutual Fund",
        headers={"Authorization": "Bearer your_expected_token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["Scheme_Name"] == "HDFC Income Fund - Normal IDCW Option"

# Mocking API failure for fetching mutual funds
@patch("app.mutual_funds.httpx.AsyncClient")
async def test_fetch_funds_api_failure(mock_client):
    mock_instance = AsyncMock()
    mock_client.return_value = mock_instance

    # Setup the mock response for failure
    mock_response = AsyncMock()
    mock_response.status_code = 500
    mock_response.json = AsyncMock(return_value={"detail": "Error fetching data"})

    # Ensure that the __aenter__ method of the AsyncMock instance returns the mock response
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.get.return_value = mock_response

    response = client.get(
        "/funds/HDFC Mutual Fund",
        headers={"Authorization": "Bearer your_expected_token"}
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching data"}

# Test buying mutual fund units with valid token
def test_buy_units_success():
    response = client.post(
        "/buy",
        headers={"Authorization": "Bearer your_expected_token"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Purchase successful!"}

# Test buying mutual fund units with invalid token
def test_buy_units_invalid_token():
    response = client.post(
        "/buy",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
