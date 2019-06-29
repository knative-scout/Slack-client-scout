from flask import Flask
import processRequest
from config.loggingfilter import *
from config.panic import *
from config.logger import *


app = Flask(__name__)


# Event listener from slack
# Parse the request payload
# Requests can be of type interactive messages or messages with direct mentions
@app.route("/listening", methods=["GET", "POST"])
def incoming_messages():
    try:
        logger.debug(request)
        if 'payload' in request.form:
            try:
                ret_resp = processRequest.get_interactive_responses()


                return Response(json.dumps(ret_resp), status=200, mimetype='application/json')
            except Exception as e:
                raise_exception("Exception while processing payload", str(e))
        else:
            try:
                ret_resp = processRequest.get_generic_responses()


                return Response(json.dumps(ret_resp), status=200, mimetype='application/json')
            except Exception as e:
                raise_exception("Exception while getting generic response", str(e))

    except Exception as e:
        return_exception("Error in Incoming Message", str(e), 404)


@app.route('/health', methods=['GET', 'POST'])
@disable_logging
def health_check():
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
