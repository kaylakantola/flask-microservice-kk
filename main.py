import os
import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

shoutcloud_url = "HTTP://API.SHOUTCLOUD.IO/V1/SHOUT"
shoutcloud_headers = { 'Content-Type': 'application/json' }


@app.route("/", methods=["POST"])
def hello_world():
    try:
        request_data_json = json.loads(request.data.decode('utf-8'))
        shoutcloud_payload = {"INPUT": request_data_json['data']}
        shoutcloud_response = requests.request("POST", url=shoutcloud_url, headers=shoutcloud_headers, json=shoutcloud_payload)
        shotcloud_response_json = shoutcloud_response.json()
        shoutcloud_output = shotcloud_response_json['OUTPUT']
        shoutcloud_output_reversed = shoutcloud_output[::-1]
        endpoint_response = {"data": shoutcloud_output_reversed}
        return endpoint_response
    except Exception as err:
        print(err)
        return "oh no"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
