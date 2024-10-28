
# HTTPie Testing Framework

## Overview
This repository provides a comprehensive testing framework for HTTPie, covering unit, functional, integration and performance testing. A sample Flask app is included to simulate different HTTP responses for broader testing needs.

## Folder Structure
- **flask_app/**: Contains a sample Flask application with custom endpoints to simulate various HTTP status codes (e.g., 200, 300, 400, 500) for testing scenarios.
- **tests/**: Houses test scripts that cover HTTPie’s request parsing, response formatting, session management, authentication and additional key functionality.

## Requirements
This project requires the following core dependencies:
- **Python** 3.10
- **HTTPie** - A modern command-line HTTP client for testing API requests.
- **Flask** - A micro web framework for creating the sample application used in testing.
- **pytest** - A robust testing framework for discovering and running tests.
- **pytest-cov** - A plugin for `pytest` to generate test coverage reports.

### Setting Up the Environment
Ensure **Miniconda** is installed to manage dependencies and the environment effectively. Then, follow these steps to create and activate the environment using the provided `environment.yml` file:

1. **Create the Environment**:
   ```bash
   conda env create -f environment.yml
   ```
2. **Activate the Environment**:
   ```bash
   conda activate httpie-testing
   ```

This setup ensures that all dependencies, including HTTPie and Flask, are installed and ready for testing.

## Running the Flask Application
The included Flask app provides various HTTP responses for testing. To start the application, navigate to the `flask_app` directory and execute:

```bash
cd flask_app
python app.py
```

This will start the Flask application, allowing HTTPie requests to be tested against different endpoints for a full spectrum of HTTP response codes.

## Running Tests
Testing is managed through **Pytest**, with optional coverage reporting provided by `pytest-cov`. 

1. **Run All Tests**:
   Execute the entire test suite, covering all core functionalities of the HTTPie testing framework.
   ```bash
   pytest --cov=tests
   ```

2. **Run a Specific Test**:
   To run an individual test, specify its path as shown below.
   ```bash
   pytest tests/test_request_parsing.py
   ```

3. **Generate Coverage Report**:
   For a comprehensive view of test coverage, run the following to generate an HTML report.
   ```bash
   pytest --cov=tests --cov-report=html
   ```

## Test Coverage
Test coverage reports are generated in HTML format, viewable under the `htmlcov` directory. These reports provide insights into the extent of test coverage for each module.

## License
This project is open-source and available under the MIT License.

For any questions or contributions, please feel free to submit issues or pull requests.

---