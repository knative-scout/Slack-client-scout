from flask import Response
import json


def raise_exception(key,value):
    status = dict()
    status[key] = value
    raise Exception(status)


def return_exception(key,value,statuscode):
    status = dict()
    status[key] = value
    return Response(json.dumps(status), status=statuscode, mimetype='application/json')