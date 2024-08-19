from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import logging
from flask_cors import CORS, cross_origin
import time
import os
from query_processing.query_processor import process_query
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['userQuery']
    current_summary = request.json['currentSummary']


    chatbot_response = process_query(user_input, current_summary)


    llama_response = chatbot_response[0]
    urls = chatbot_response[1]
    llama_resp_obj = {
    "agentName": "LLaMa 3.1",
    "agentResponse": llama_response,
    "urls": urls
    }
    summary = chatbot_response[2]

    rlist = [llama_resp_obj, summary]
    response = jsonify(rlist)
    return response





if __name__ == '__main__':
    app.run()
