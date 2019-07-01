from flask import Flask
import processRequest
from config.config import bot_token
from config.loggingfilter import *
from config.panic import *
from slack import WebClient


slack = WebClient(token=bot_token)


app = Flask(__name__)


# Event listener from slack
# Parse the request payload
# Requests can be of type interactive messages or messages with direct mentions
@app.route("/listening", methods=["GET", "POST"])
def incoming_messages():
    try:
        if 'payload' in request.form:
            try:
                ret_resp = processRequest.get_interactive_responses()
                if not isinstance(ret_resp, str):
                    slack.chat_postMessage(
                        token=bot_token,
                        channel = ret_resp.channel,
                        text = ret_resp.text,
                        attachments = ret_resp.attachments,
                    )
                else:
                    return Response(json.dumps(ret_resp), status=200, mimetype='application/json')
            except Exception as e:
                raise_exception("Exception while processing payload", str(e))
        else:
            try:
                print (request.get_json())
                ret_resp = processRequest.get_generic_responses()
                if not isinstance(ret_resp, str):
                    print(ret_resp.channel)
                    slack.chat_postMessage(
                        token=bot_token,
                        channel = ret_resp.channel,
                        text = ret_resp.text,
                        attachments = ret_resp.attachments,
                    )
                else:
                    return Response(json.dumps(ret_resp), status=200, mimetype='application/json')
            except Exception as e:
                raise_exception("Exception while getting generic response", str(e))

    except Exception as e:
        print (str(e))
        return_exception("Error in Incoming Message", str(e), 404)

    return_exception("Internal Server Error", "No Message from Server", 404)


@app.route('/health', methods=['GET', 'POST'])
@disable_logging
def health_check():
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
