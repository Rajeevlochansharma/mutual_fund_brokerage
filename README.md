# Mutual Fund Brokerage

Project Structure Documentation

mutual_fund_brokerage/
│
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI main file: Entry point for the application, defines API endpoints and app configuration.
│   │   ├── auth.py           # Authentication logic: Handles user authentication and token management.
│   │   ├── mutual_funds.py   # Mutual fund-related logic: Contains functions for fetching and managing mutual fund data.
│   ├── tests/                # Directory for end-to-end tests: Contains test files to validate API functionality.
│   │   ├── test_main.py      # Main E2E test file: Tests the API endpoints for login, fetching funds, and buying units.
│   ├── static/               # Frontend assets (HTML, JS, CSS): Contains web files served to the client.
│   │   ├── login.html        # Login page: HTML file for user login interface.
│   │   ├── dashboard.html    # Dashboard page: HTML file for displaying mutual fund information and user actions.
│   │   ├── styles.css        # Optional CSS for styling: Contains styles for the HTML pages.
│   └── venv                  # Virtual Environment: Directory containing the virtual environment for package management.
│   └── .env                  # Environment file: Stores environment variables such as API keys and dummy credentials.
└── requirements.txt          # Required packages: Lists all the Python packages required to run the application.
└── pytest.ini                # Configuration file for pytest: Specifies test settings and configurations for running tests.

## Getting Started
Prerequisites
	Python 3.7 or higher
	pip (Python package manager)

## Installation
1. Clone the repository:
	git clone https://github.com/Rajeevlochansharma/mutual_fund_brokerage.git
	cd mutual_fund_brokerage

2. Set up the virtual environment:
	cd backend
	python -m venv venv

3. Activate the virtual environment:
	For Windows:
		venv\Scripts\activate
	For macOS/Linux:
		source venv/bin/activate

4. Install required packages:
	pip install -r requirements.txt

5. Set up environment variables:
	Create a .env file in the backend directory and add your API key and dummy credentials:
		RAPIDAPI_KEY=your_rapidapi_key

## Running the Application
1. Start the FastAPI server:
	uvicorn app.main:app --reload

2. Access the application:
	Navigate to http://127.0.0.1:8000/static/login.html in your web browser to access the login page.

## Endpoints Overview
1. POST /token:
	Authenticates the user and returns a token.
	Request body: { "username": "string", "password": "string" }

2. GET /funds/{fund_family}:
	Fetches open-ended schemes for the selected fund family.
	Requires a token in the Authorization header.
	
3. POST /buy:
	Initiates the purchase of mutual fund units.
	Requires a token in the Authorization header.
	
## Frontend
1. login.html:
	Provides a login interface.
	
2. dashboard.html:
	Displays available mutual funds and allows users to make purchases.
	
## Testing
1. E2E Tests
	Navigate to the tests directory:
		cd tests

2. Run the tests:
	Ensure you have your virtual environment activated and run:
		pytest -v

3. Test Overview
	The test_main.py file contains tests for:
		Successful login
		Fetching funds
		Buying mutual fund units
		
4. Mocking External API Calls
	In the test_main.py, you can use libraries like pytest and httpx to mock the external API calls made in mutual_funds.py. This ensures your tests run without making real HTTP requests.
	
## File-Specific Documentation
1. main.py
	Purpose: Serves as the main entry point for the FastAPI application.
	Key Features:
		Sets up CORS middleware to allow cross-origin requests.
		Defines API endpoints for login, fetching mutual fund details, and purchasing units.
		Uses dependency injection to manage authentication tokens.
		
2. auth.py
	Purpose: Manages user authentication.
	Key Features:
		Defines functions for authenticating users and generating tokens.
		Implements a fake token decoder for test purposes.
		
3. mutual_funds.py
	Purpose: Contains logic related to mutual funds.
	Key Features:
		Implements a function to fetch open-ended mutual fund schemes from an external API.
		Handles the HTTP requests and responses.
		
4. tests/test_main.py
	Purpose: Contains end-to-end tests for the application.
	Key Features:
		Tests the login functionality for valid and invalid credentials.
		Mocks external API calls to test fetching mutual fund data and handles API failure scenarios.
		Tests purchasing functionality to ensure proper responses for valid and invalid tokens.
		
5. static/
	Purpose: Contains static files for the frontend.
	Files:
		login.html: HTML interface for user login.
		dashboard.html: Displays mutual fund data and user actions.
		styles.css: Styles for the HTML pages.

6. .env
	Purpose: Stores sensitive information and configuration variables, such as API keys and credentials.
	Usage: Loaded at runtime to configure the application environment.

7. requirements.txt
	Purpose: Lists all necessary Python packages for the project.
	Usage: Used to install dependencies with pip install -r requirements.txt.

8. pytest.ini
	Purpose: Configures pytest for running tests.
	Key Features:
		Can specify options such as test paths, markers, and other settings to customize test runs.

## Postman Collection Overview
Collection Name: Mutual Fund Brokerage API
1. Login Endpoint
	Request Type: POST
	URL: http://localhost:8000/token
	Body (JSON):
		{
		  "username": "admin",
		  "password": "admin123"
		}
	Success Response:
		Status: 200 OK
		Body:
			{
			  "access_token": "your_expected_token",
			  "token_type": "bearer"
			}
	Failure Response:
		Request:
			{
			  "username": "wronguser",
			  "password": "wrongpass"
			}
		Status: 401 Unauthorized
		Body:
			{
			  "detail": "Invalid credentials"
			}

2. Fetch Funds Endpoint
	Request Type: GET
	URL: http://localhost:8000/funds/HDFC Mutual Fund
	Headers:
		Authorization: Bearer your_expected_token
	Success Response:
		Status: 200 OK
		Body:
			[
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
			]
	Failure Response:
		Request (with invalid token):
			Headers:
				Authorization: Bearer invalid_token
		Status: 401 Unauthorized
		Body:
			{
			  "detail": "Invalid token"
			}

3. Buy Units Endpoint
	Request Type: POST
	URL: http://localhost:8000/buy
	Headers:
		Authorization: Bearer your_expected_token
	Success Response:
		Status: 200 OK
		Body:
			{
				"message": "Purchase successful!"
			}
		Failure Response:
			Request (with invalid token):
				Headers:
					Authorization: Bearer invalid_token
			Status: 401 Unauthorized
			Body:
				{
				  "detail": "Invalid token"
				}

- How to Create the Collection in Postman
	1. Open Postman and click on the Collections tab.
	2. Click on the New Collection button.
	3. Name your collection (e.g., "Mutual Fund Brokerage API").
	4. Inside the collection, create a new request for each of the endpoints listed above:
		Set the method (GET or POST).
		Enter the URL.
		Add the request body (for POST requests) and headers as necessary.
		Save the responses as examples for both success and failure cases.

- Exporting the Collection
	1. Click on the three dots next to your collection name.
	2. Select Export.
	3. Choose the format (usually the default is fine) and save it.

This Postman collection will help you easily test and document the success and failure responses of your mutual fund brokerage API.

## Additional Notes
	Ensure that the .env file is properly configured with any required API keys and credentials for external services.
	When running tests, use the command pytest in the terminal, ensuring you're in the project directory where pytest.ini is located.
	Always activate your virtual environment before running the application or tests to ensure you're using the correct dependencies.
	
## Documentation
	For further details, refer to the FastAPI documentation: FastAPI Docs.

## Conclusion
	This documentation serves as a guide for understanding the structure and functionality of the mutual_fund_brokerage project. It can be expanded with additional details as the project evolves.