import os
import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

def read_input(r):
    request_data_json = json.loads(r.data.decode('utf-8'))
    return request_data_json['data']


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
        shoutcloud_payload = build_shoutcloud_payload(user_input)
        shoutcloud_response = post_to_shoutcloud(shoutcloud_payload)
        shoutcloud_response_reversed = reverse_text(shoutcloud_response)
        endpoint_response = build_endpoint_response(shoutcloud_response_reversed)
        return endpoint_response
    except Exception as err:
        print(err)
        return "oh no"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
