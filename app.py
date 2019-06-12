from flask import Flask, make_response
import processRequest
import json

app = Flask(__name__)

# Event listener from slack
@app.route("/listening", methods=["GET", "POST"])
def incoming_messages():
    # Parse the request payload
    # Requests can be of type interactive messages or messages with direct mentions
    try:
        return processRequest.get_interactive_responses()

    except:
        return processRequest.get_generic_responses()


@app.route('/health', methods=['GET', 'POST'])
def health_check():
    status = {"ok": True}
    return make_response(json.dumps(status), 200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
