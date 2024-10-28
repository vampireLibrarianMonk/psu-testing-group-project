from flask import Flask, jsonify, redirect

app = Flask(__name__)

# 1xx Informational - Example using 102 Processing
@app.route('/status/102')
def status_102():
    # Return a 102 Processing response with no content
    return '', 102

# 2xx Success - Example using 200 OK
@app.route('/status/200')
def status_200():
    # Return a JSON success message with a 200 OK status
    return jsonify({"message": "Success"}), 200

# 3xx Redirection - Example using 302 Found
@app.route('/status/302')
def status_302():
    # Redirect to the /status/200 endpoint with a 302 status
    return redirect('/status/200', code=302)

# 4xx Client Error - Example using 404 Not Found
@app.route('/status/404')
def status_404():
    # Return a JSON error message with a 404 Not Found status
    return jsonify({"error": "Not Found"}), 404

# 5xx Server Error - Example using 500 Internal Server Error
@app.route('/status/500')
def status_500():
    # Return a JSON error message with a 500 Internal Server Error status
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(port=5001)