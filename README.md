# HTTPie Testing Framework

## Overview

functionality, focusing primarily on its CLI-based usage. Given the CLI-first nature of HTTPie, many of its core features—such as session handling, plugin integration, and response formatting—are not fully exposed via its internal Python modules. This testing framework addresses that gap by executing HTTPie commands through the `subprocess.run` interface and validating the behavior against a local Flask server or external services like `httpbin.org`.

httpbin is a free and open-source HTTP testing service designed to simplify API development and testing. It provides various endpoints that allow users to simulate and inspect HTTP requests and responses. This makes it an ideal tool for debugging and validating HTTP client behaviors, such as request payloads, headers, cookies, authentication and redirection handling.

Some of the commonly used endpoints include:

    /get: Returns the query parameters of a GET request.
    /post: Echoes the data sent in a POST request.
    /status/:code: Returns a response with the specified HTTP status code.
    /redirect/:n: Simulates a series of redirects (e.g., /redirect/2 redirects twice).

For this project, httpbin complements the local Flask app by providing external endpoints to test HTTPie's functionality in real-world scenarios.

## Test Completeness

This framework focuses on testing HTTPie's CLI functionality in realistic scenarios. By leveraging subprocess.run to execute HTTPie commands, the test suite evaluates features like request handling, response formatting, session management, error handling, and authentication. Each test verifies that HTTPie behaves as expected when interacting with live or simulated endpoints.

Given the CLI-first design of HTTPie, traditional code coverage tools are not applicable for assessing HTTPie's internal modules. Instead, the framework ensures full coverage of its CLI capabilities by focusing on:

    Request Parsing: Validation of methods, headers, and payload formatting.
    Response Handling: Verification of content parsing (e.g., JSON, XML, CSV) and error reporting.
    Session Management: Testing persistent and non-persistent sessions, as well as cookie handling.
    Authentication: Testing support for Basic Auth, Bearer tokens, and custom headers.

This approach ensures robust functionality and reliability in real-world use cases, with a focus on practical outcomes over internal code coverage metrics.

## Folder Structure

The repository is organized to separate the core application, testing framework, and supporting files for clarity and maintainability:

    flask_app/:
    Contains the Flask application, app.py, which simulates various HTTP scenarios. It provides endpoints for testing status codes, authentication, session handling, cookie management, and payload handling. This app serves as the primary target for HTTPie CLI tests.

    tests/:
    Contains CLI-based test scripts for validating HTTPie’s functionality across multiple scenarios:
        test_authentication.py: Tests HTTPie’s support for Basic Authentication, ensuring valid and invalid credentials are handled correctly.
        test_command_line.py: Validates the parsing of command-line arguments, including HTTP methods, headers, and data payloads.
        test_error_handling.py: Covers how HTTPie handles various HTTP error responses, such as 404 (Not Found) and 500 (Internal Server Error).
        test_file_download.py: Tests HTTPie’s file download capabilities, verifying file integrity through MD5 checksum validation.
        test_performance.py: Evaluates performance by simulating high-volume requests and testing HTTPie’s ability to handle large payloads.
        test_plugin_system.py: Validates HTTPie’s integration with custom authentication plugins, such as Bearer token support.
        test_request_parsing.py: Focuses on HTTP request parsing, ensuring methods, URLs, and headers are processed correctly.
        test_response_formatting.py: Tests handling of various response formats, including JSON, XML, CSV, and HTML payloads.
        test_session_management.py: Covers session-related features such as header persistence, cookie management, and session reuse.

    environment.yml:
    Defines the Conda environment setup, specifying Python, HTTPie, Flask, and other dependencies required to run the tests consistently.

Each file is tailored to cover a specific aspect of HTTPie’s functionality, ensuring comprehensive testing of its CLI behavior.

## Requirements
This project used the following core tools:

    Conda: 24.9.2
    Pip: 24.2
    Python: 3.10.0
    Pycharm: 2024.2.3

Primary Dependencies

The key libraries and tools necessary to run the framework include:

    HTTPie: A modern command-line HTTP client for API testing (v3.2.3).
    Flask: A lightweight web framework for creating the local testing server (v3.0.3).
    Pytest: A robust testing framework for managing and executing test cases (v8.3.3).
    Pytest-Cov: A plugin for generating test coverage reports (v5.0.0).
    Requests: A simple, yet powerful HTTP library for Python (v2.31.0).

### Setting up the IDE
To install PyCharm 2024.2.3 on your Linux system, follow these steps:

1. Download PyCharm:

Visit the official JetBrains website to download the PyCharm tarball for Linux:

[PyCharm Download Page](https://www.jetbrains.com/pycharm/download/)

Choose the appropriate edition (Professional or Community) and download the .tar.gz file.

2. Extract the Tarball:

Open a terminal and navigate to the directory where the tarball was downloaded. Extract it using the following command:
```bash
tar -xzf pycharm-2024.2.3.tar.gz
```

Replace pycharm-2024.2.3.tar.gz with the actual filename if it differs.

3. Move to the Installation Directory:

It's recommended to move the extracted folder to /opt/ for system-wide availability:
```bash
sudo mv pycharm-2024.2.3 /opt/pycharm-2024.2.3
```

4. Create a Symbolic Link:

For easier access, create a symbolic link:

```bash
sudo ln -s /opt/pycharm-2024.2.3/bin/pycharm.sh /usr/local/bin/pycharm
```

5. Launch PyCharm:

Start PyCharm by running:
```bash
pycharm
```

Alternatively, navigate to /opt/pycharm-2024.2.3/bin/ and execute pycharm.sh:

```bash
cd /opt/pycharm-2024.2.3/bin/
./pycharm.sh
```

6. Optional: Create a Desktop Entry:

To add PyCharm to your application menu:

Open PyCharm.
Navigate to Tools > Create Desktop Entry.
Follow the prompts to create the entry.
This will allow you to launch PyCharm from your desktop environment's application menu.

Note: Ensure you have the necessary permissions to install software on your system. For more detailed instructions, refer to the [PyCharm Installation Guide](https://www.jetbrains.com/help/pycharm/installation-guide.html).

### Setting Up the Environment
To run this project, you need to set up a Conda environment on your Linux system (Windows is not supported). Follow these steps to install Miniconda, create the environment, and activate it:

1. Installing Miniconda on Linux
Download and install Miniconda by following these steps:

2. Download the Miniconda Installer:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

3. Verify the Installer (Optional): Check the integrity of the downloaded file using its SHA256 hash (available on the Miniconda website).
```bash
sha256sum Miniconda3-latest-Linux-x86_64.sh
```

4. Run the Installer: Execute the installer script:
```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

5. Follow the prompts to complete the installation. Make sure to allow the installer to modify your ~/.bashrc file for easier access to Conda commands.

6. Activate Conda: Refresh your shell or manually activate Conda:
```bash
source ~/.bashrc
````

7.Verify Installation: Ensure Miniconda is installed:
```bash
conda --version
```

8. Navigate to the Project Directory:
```bash
cd /path/to/your/project
```

9. Create the Conda Environment: Use the provided environment.yml file to create the environment:
```bash
conda env create -f environment.yml
```

10. Activating the Environment
Once the environment is created, activate it using:
```bash
conda activate httpie-testing
```

## Setting up conda environment within Pycharm
1. Launch PyCharm and open an existing project or create a new one.

2. Navigate to File > Settings (Preferences on macOS) > Project: [Your Project Name] > Python Interpreter.

3. Click the gear icon next to the interpreter selection and choose "Add Interpreter".

4. In the Add Python Interpreter dialog, choose "Conda Environment".

5: Configure the Conda Environment
 Option 1: Use an Existing Environment
 - Select "Existing Environment".
 - Browse to the environment's Python binary, e.g.:
   /home/your-user/miniconda3/envs/httpie-testing/bin/python
 - Click "OK".

 Option 2: Create a New Environment
 - Select "New Environment".
 - Choose a location for the environment (e.g., within your Conda installation).
 - Specify Python 3.10 as the interpreter.

6. Click "OK" or "Apply". PyCharm will index the environment.

7. Open the PyCharm Terminal and run:
```bash
conda env update -f environment.yml
```

8. Verify the Setup
 Go to File > Settings > Project: [Your Project Name] > Python Interpreter
 Ensure the interpreter path points to your Conda environment.
 Open a Python file to verify dependencies and imports are recognized.

## Running the Flask Application

The included Flask app provides various HTTP responses for testing. To start the application, navigate to the `flask_app` directory and execute:

```bash
cd flask_app
python app.py
```

This will start the Flask application, allowing HTTPie requests to be tested against different endpoints for a full spectrum of HTTP response codes.

Expected Output:
```bash
* Serving Flask app 'app'
 * Debug mode: off
 WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001
 Press CTRL+C to quit
```

## Running Tests

Testing is managed through **Pytest** and involves executing HTTPie CLI commands via `subprocess.run`. Each test script runs HTTPie commands against the Flask app or external endpoints (e.g., `httpbin.org`) to validate expected behaviors such as response parsing, header management, and authentication.

0. Ensure the flask is running:

1. **Run All Tests**:
    Execute the entire CLI-based test suite, capturing and verifying outputs from HTTPie commands.
    ```bash
    python flask_app/app.py
    ```

    Execute the entire test suite, covering all core functionalities of the HTTPie testing framework.
    ```bash
    pytest --cov=tests
    ```

Example Output:
    ```bash
    ================================================================ test session starts ================================================================
    platform linux -- Python 3.10.0, pytest-8.3.3, pluggy-1.5.0
    rootdir: /home/esquire-incarnate/Documents/Code/pre-project/httpie-testing
    plugins: cov-5.0.0
    collected 49 items                                                                                                                                  
    
    tests/test_authentication.py ......                                                                                                           [ 12%]
    tests/test_command_line.py ..............                                                                                                     [ 40%]
    tests/test_error_handling.py .....                                                                                                            [ 51%]
    tests/test_file_download.py .                                                                                                                 [ 53%]
    tests/test_performance.py ..                                                                                                                  [ 57%]
    tests/test_plugin_system.py ..                                                                                                                [ 61%]
    tests/test_request_parsing.py ...                                                                                                             [ 67%]
    tests/test_response_formatting.py ....                                                                                                        [ 75%]
    tests/test_session_management.py ............                                                                                                 [100%]
    
    ---------- coverage: platform linux, python 3.10.0-final-0 -----------
    Name                                Stmts   Miss  Cover
    -------------------------------------------------------
    tests/__init__.py                       0      0   100%
    tests/test_authentication.py           38      1    97%
    tests/test_command_line.py             87     10    89%
    tests/test_error_handling.py           40      3    92%
    tests/test_file_download.py            28      1    96%
    tests/test_performance.py              53     11    79%
    tests/test_plugin_system.py            24      1    96%
    tests/test_request_parsing.py          13      1    92%
    tests/test_response_formatting.py      62      1    98%
    tests/test_session_management.py       71      1    99%
    -------------------------------------------------------
    TOTAL                                 416     30    93%
    
    
    ========================================================== 49 passed in 181.69s (0:03:01) ===========================================================
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

   The above command will generate a htmlcov directory in which you will open the index.html to see your coverage report that is more interactive than the output from just running the command line.

## License

This project is open-source and available under the MIT License.

For any questions or contributions, please feel free to submit issues or pull requests.
