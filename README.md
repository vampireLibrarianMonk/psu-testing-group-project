# HTTPie Testing Framework

## Overview

This repository provides a comprehensive testing framework for HTTPie, focusing on CLI-based testing due to the limited functionality exposed via HTTPie’s internal Python modules. Initially, the framework was designed to access HTTPie’s internals directly. However, further research revealed that many core features, such as plugin loading, session handling and response formatting, are optimized for the CLI and are either unavailable or restricted when accessed programmatically in Python. As a result, testing has shifted to executing HTTPie CLI commands through `subprocess.run` and validating outputs against a live or locally hosted server (e.g., `httpbin.org` or the included Flask application).

This approach accurately captures HTTPie’s behavior in real-world usage scenarios, ensuring that all tested features are as HTTPie CLI users would experience them.

## Test Completeness

Since this test suite operates via HTTPie’s CLI, traditional code coverage tools do not provide meaningful insights into HTTPie’s internal structure. Instead, this suite focuses on testing the full range of HTTPie’s CLI capabilities, including request handling, response formatting, session management, and error handling. The tests aim to validate HTTPie’s behavior in practical use cases, ensuring robust and reliable functionality in real-world scenarios.

## Folder Structure

- **flask_app/**: Contains a sample Flask application with custom endpoints to simulate various HTTP status codes (e.g., 200, 300, 400, 500) for testing scenarios.
- **tests/**: Houses CLI-based test scripts that cover HTTPie’s request parsing, response formatting, session management, authentication, and error handling.

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

Testing is managed through **Pytest** and involves executing HTTPie CLI commands via `subprocess.run`. Each test script runs HTTPie commands against the Flask app or external endpoints (e.g., `httpbin.org`) to validate expected behaviors such as response parsing, header management, and authentication.

1. **Run All Tests**:
   Execute the entire CLI-based test suite, capturing and verifying outputs from HTTPie commands.

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
While traditional coverage metrics don’t apply to HTTPie’s internal code due to CLI testing, you can still generate a coverage report for the test scripts themselves:

   ```bash
   pytest --cov=tests --cov-report=html
   ```

## License

This project is open-source and available under the MIT License.

For any questions or contributions, please feel free to submit issues or pull requests.
