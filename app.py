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
    model_selection = request.json['modelSelection']
    user_input = request.json['userQuery']
    current_summary = request.json['currentSummary']

    # response: [gpt_response, llama_response, summary]
    # model response object: {"agentName": "", "agentResp": "", "urls": [], "summary": ""}


    chatbot_response = process_query(user_input, model_selection, current_summary)

    if model_selection == "gpt":
        gpt_response = chatbot_response[0]
        urls = chatbot_response[1]
        gpt_resp_obj = {
        "agentName": "GPT-4o",
        "agentResponse": gpt_response,
        "urls": urls
        } 

        summary = chatbot_response[2]

        rlist = [gpt_resp_obj, summary]
        response = jsonify(rlist)
        return response
    

    elif model_selection == "llama":
        llama_response = chatbot_response[0]
        urls = chatbot_response[1]
        llama_resp_obj = {
        "agentName": "LLaMa-3",
        "agentResponse": llama_response,
        "urls": urls
        }
        summary = chatbot_response[2]

        rlist = [llama_resp_obj, summary]
        response = jsonify(rlist)
        return response
    else:
        gpt_response = chatbot_response[0]
        llama_response = chatbot_response[1]
        urls = chatbot_response[2]
        gpt_resp_obj = {
        "agentName": "GPT-4o",
        "agentResponse": gpt_response,
        "urls": urls
        } 
        llama_resp_obj = {
        "agentName": "LLaMa-3",
        "agentResponse": llama_response,
        "urls": urls
        }
        summary = chatbot_response[3]

        rlist = [gpt_resp_obj, llama_resp_obj, summary]
        response = jsonify(rlist)
        return response





if __name__ == '__main__':
    app.run()
