# DummyJSON API Tests

API automation testing framework for [DummyJSON](https://dummyjson.com) with Allure reporting.

## Features

- **Clean Architecture**: Organized structure with separate layers for base classes, API clients, models, and tests
- **Type Safety**: Pydantic models for API request/response validation
- **Allure Reports**: Beautiful HTML test reports with detailed test execution information
- **pytest Integration**: Powerful testing framework with fixtures and parametrization
- **HTTP Client**: Robust HTTP client with retry logic and logging
- **Code Quality**: Ruff linting and formatting

## Project Structure

```
dummyjson-api-tests/
├── base/                          # Base classes and utilities
│   ├── api/
│   │   └── api_client.py         # HTTP client with retry logic
│   └── models/
│       └── base_model.py         # Base Pydantic model
├── dummyjson/                    # DummyJSON-specific code
│   ├── clients/                  # API clients for different endpoints
│   │   ├── product_client.py
│   │   ├── user_client.py
│   │   └── auth_client.py
│   ├── models/                   # Pydantic models for API responses
│   │   ├── product.py
│   │   ├── user.py
│   │   └── auth.py
│   └── tests/
│       └── api/                  # API tests
│           ├── test_products.py
│           ├── test_users.py
│           └── test_auth.py
├── tools/                        # Helper scripts
│   └── run_with_allure.py        # Run tests with Allure report
├── conftest.py                   # pytest fixtures
├── pyproject.toml                # Project dependencies and configuration
└── README.md

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- [Allure CLI](https://docs.qameta.io/allure/) (for generating reports)

## Installation

### 1. Install uv

- **macOS (Homebrew)**:
  ```bash
  brew install uv
  ```

- **Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **Windows (PowerShell)**:
  ```powershell
  powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex"
  ```

### 2. Install Python 3.12

```bash
uv python install 3.12
```

### 3. Install Allure CLI

- **macOS**:
  ```bash
  brew install allure
  ```

- **Linux/Windows**: Follow instructions at [Allure Docs](https://docs.qameta.io/allure/#_installing_a_commandline)

### 4. Clone the repository

```bash
git clone https://github.com/ssamhawk/dummyjson-api-tests.git
cd dummyjson-api-tests
```

### 5. Install dependencies

```bash
uv sync
```

## Running Tests

### Run all tests

```bash
uv run pytest -v
```

### Run specific test file

```bash
uv run pytest dummyjson/tests/api/test_products.py -v
```

### Run tests with specific marker

```bash
uv run pytest -v -m "not slow"
```

### Run with Allure report

```bash
uv run pytest --alluredir=allure-results
allure serve allure-results
```

### Using the Allure helper script

```bash
uv run python tools/run_with_allure.py --open
```

## Code Quality

### Run linter

```bash
uv run ruff check .
```

### Auto-fix linting issues

```bash
uv run ruff check . --fix
```

### Format code

```bash
uv run ruff format .
```

## Test Coverage

The framework covers the following DummyJSON API endpoints:

### Products API
- Get all products with pagination
- Get single product by ID
- Search products
- Get products by category
- Get all categories
- Add/Update/Delete products

### Users API
- Get all users with pagination
- Get single user by ID
- Search users
- Filter users
- Add/Update/Delete users

### Authentication API
- Login with credentials
- Get current authenticated user
- Refresh access token

## API Documentation

For more information about the DummyJSON API, visit [https://dummyjson.com/docs](https://dummyjson.com/docs)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is open source and available under the MIT License.
