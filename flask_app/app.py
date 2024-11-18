from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

# Token variables for customization
tokenValue = "sampletoken"
userValue = "anonymousDude"

#-------------------------------------------------------------------------------
# 1xx Informational Responses
#-------------------------------------------------------------------------------

@app.route('/status/102', methods=['GET'])
def status_102():
    """
    Handle the route for a 102 Processing status.

    Returns:
        Response: A JSON object with a "Processing" message.
        int: HTTP status code 102.

    This endpoint simulates an informational response, which is not directly
    handled by HTTPie. For testing, we mimic this with a message.
    """
    return jsonify({"status": "Processing", "note": "This simulates a 102 response"}), 200

#-------------------------------------------------------------------------------
# 2xx Successful Responses
#-------------------------------------------------------------------------------

@app.route('/status/200', methods=['GET'])
def status_200():
    """
    Handle the route for a 200 OK status.

    Returns:
        Response: A JSON object with a success message.
        int: HTTP status code 200 to indicate a successful request.

    This endpoint simulates a standard success response, commonly used to indicate
    that the request was processed successfully.
    """
    return jsonify({"message": "Success"}), 200

#-------------------------------------------------------------------------------
# 3xx Redirection Responses
#-------------------------------------------------------------------------------

@app.route('/status/302', methods=['GET'])
def status_302():
    """
    Handle the route for a 302 Found status.

    Redirects:
        str: The URL to redirect the client to, in this case, '/status/200'.
        int: HTTP status code 302 to indicate a redirection.

    This endpoint simulates a redirection, instructing the client to fetch the
    resource at '/status/200'.
    """
    return redirect('/status/200', code=302)

#-------------------------------------------------------------------------------
# 4xx Client Error Responses
#-------------------------------------------------------------------------------

@app.route('/status/404', methods=['GET'])
def status_404():
    """
    Handle the route for a 404 Not Found status.

    Returns:
        Response: A JSON object with an error message.
        int: HTTP status code 404 to indicate that the requested resource was not found.

    This endpoint simulates a client error response, typically used when the requested
    resource does not exist on the server.
    """
    return jsonify({"error": "Not Found"}), 404

#-------------------------------------------------------------------------------
# 5xx Server Error Responses
#-------------------------------------------------------------------------------

@app.route('/status/500', methods=['GET'])
def status_500():
    """
    Handle the route for a 500 Internal Server Error status.

    Returns:
        Response: A JSON object with an error message.
        int: HTTP status code 500 to indicate a generic server error.

    This endpoint simulates a server error response, typically used when the server
    encounters an unexpected condition that prevents it from fulfilling the request.
    """
    return jsonify({"error": "Internal Server Error"}), 500

#-------------------------------------------------------------------------------
# Custom Routes for Session Management and Testing
#-------------------------------------------------------------------------------

@app.route('/test/headers', methods=['GET', 'POST'])
def test_headers():
    """
    Handle the route for testing header persistence.

    Checks for the 'Authorization' header in the request and verifies if it matches
    the expected values.

    Returns:
        Response: A JSON object with a success or error message.
        int: HTTP status code 200 if the header is correct, 401 otherwise.

    This endpoint is used to test if authorization headers persist across
    different requests, which is crucial for session management and security.
    """
    auth_header = request.headers.get('Authorization')
    if auth_header in [f"Bearer {tokenValue}", f"Bearer {userValue}"]:
        return jsonify({"message": "Authorization header received"}), 200
    return jsonify({"error": "Authorization header missing or incorrect"}), 401

@app.route('/test/basic-auth', methods=['GET'])
def basic_auth():
    """
    Handle the route for testing basic authentication.

    Checks the 'Authorization' header for basic authentication credentials and
    verifies if they are correct.

    Returns:
        Response: A JSON object with a success or error message.
        int: HTTP status code 200 if the credentials are correct, 401 otherwise.

    This endpoint is used to test basic authentication mechanisms, ensuring that
    the server correctly handles and validates user credentials.
    """
    auth = request.authorization
    if auth and auth.username == 'user1' and auth.password == 'password':
        return jsonify({"message": "Basic Auth successful"}), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/test/large_payload', methods=['POST'])
def large_payload():
    """
    Handle the route for testing large payloads in session.

    Accepts a large payload in the request and verifies if it can be processed
    and stored correctly.

    Returns:
        Response: A JSON object confirming receipt of the payload.
        int: HTTP status code 200 if the payload is successfully received.
    """
    payload = request.form.get('payload')
    if payload:
        return jsonify({"status": "Payload received", "payload_size": len(payload)}), 200
    return jsonify({"error": "Payload not provided"}), 400

#-------------------------------------------------------------------------------
# Main Entry Point
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Main entry point of the Flask application.

    Runs the Flask development server on port 5001, making the app accessible
    locally at 'http://localhost:5001'.
    """
    app.run(port=5001)
