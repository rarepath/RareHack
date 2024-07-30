from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import logging
from flask_cors import CORS, cross_origin
import time
import os
# from query_processing.query_processor import process_query
logging.basicConfig(level=logging.DEBUG)

# initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True, origins=["https://localhost:4200"])

@app.route('/get_response', methods=['POST', 'OPTIONS'])
@cross_origin(origin='http://localhost:4200', supports_credentials=True)  # Ensure correct origin
def get_response():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    if request.method == 'POST':
        gpt_response = "generic gpt response"
        llama_response = "generic llama response"
        urls = ["url1", 'url2', 'url3']
        gpt_resp_obj = {
        "agentName": "GPT-4o",
        "agentResponse": gpt_response,
        "urls": urls
        } 
        llama_resp_obj = {
        "agentName": "llama-3", 
        "agentResponse": llama_response,
        "urls": urls
        }
        summary = "this is a development summary for testing"

        rlist = [gpt_resp_obj, llama_resp_obj, summary]
        response = jsonify(rlist)
        return response




if __name__ == '__main__':
    app.run(debug=True)
