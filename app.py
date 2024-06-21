from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import logging
from flask_cors import CORS
import time
import os
from query_processing.query_processor import process_query
logging.basicConfig(level=logging.DEBUG)

# initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

@app.route('/get_response', methods=['POST'])
def get_response():
    model_selection = request.json['modelSelection']
    user_input = request.json['userQuery']
    current_summary = request.json['currentSummary']

    # response: [gpt_response, llama_response, summary]
    # model response object: {"agentName": "", "agentResp": "", "urls": [], "summary": ""}
    chatbot_response = process_query(user_input, current_summary)

    gpt_response = chatbot_response[0]
    llama_response = chatbot_response[1]
    gpt_resp_obj = gpt_response = {
    "agentName": "GPT-4-turbo",
    "agentResponse": gpt_response,
    "urls": [
      "gpt.com",
        ]
    }
    llama_resp_obj = {
    "agentName": "llama-3",
    "agentResponse": llama_response,
    "urls": [
      "ollama.com"
        ]
    }
    summary = chatbot_response[2]
    
    rlist = [gpt_resp_obj, llama_resp_obj, summary]
    response = jsonify(rlist)
    return response


if __name__ == '__main__':
    app.run(debug=True)
