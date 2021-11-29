import json
from flask import Flask, request
import requests

app = Flask(__name__)


def read_input(r):
    request_data_json = json.loads(r.data.decode('utf-8'))
    return request_data_json


def validate_input(user_input):
    if 'data' not in user_input:
        return False

    if type(user_input['data']) != str:
        return False

    if len(user_input['data']) < 1:
        return False

    return True


def build_shoutcloud_payload(input):
    shoutcloud_payload = {"INPUT": input}
    return shoutcloud_payload


def post_to_shoutcloud(json_data):
    shoutcloud_url = "HTTP://API.SHOUTCLOUD.IO/V1/SHOUT"
    shoutcloud_headers = { 'Content-Type': 'application/json' }
    shoutcloud_response = requests.request("POST", url=shoutcloud_url, headers=shoutcloud_headers, json=json_data)
    shotcloud_response_json = shoutcloud_response.json()
    shoutcloud_output = shotcloud_response_json['OUTPUT']
    return shoutcloud_output


def reverse_text(text):
    return text[::-1]


def build_endpoint_response(text):
    return {"data": text}


@app.route("/", methods=["POST"])
def reverse_shout():
    try:
        user_input = read_input(request)
        valid_input = validate_input(user_input)

        if valid_input is False:
            return {"error": f"Request body must contain 'data' parameter set to a string with a length greater than 0."}, 400

        shoutcloud_payload = build_shoutcloud_payload(user_input['data'])
        shoutcloud_response = post_to_shoutcloud(shoutcloud_payload)
        shoutcloud_response_reversed = reverse_text(shoutcloud_response)
        endpoint_response = build_endpoint_response(shoutcloud_response_reversed)
        return endpoint_response
    except Exception as err:
        return {"error": f"Something broke, here's a hint: {err}"}, 500


# Load testing
@app.route("/loaderio-6d44e3a83fc245de7faff2cc9041d61f.txt")
def loader():
    return 'loaderio-6d44e3a83fc245de7faff2cc9041d61f'
