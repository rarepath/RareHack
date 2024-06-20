from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import logging
from flask_cors import CORS
import time

# configure loggin
logging.basicConfig(level=logging.DEBUG)

# initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

@app.route('/get_response', methods=['POST'])
def get_response():
    model_selction = request.json['modelSelection']
    user_input = request.json['userQuery']
    current_summary = request.json['currentSummary']

    # response: [gpt_response, llama_response, summary]
    # model response object: {"agentName": "", "agentResp": "", "urls": [], "summary": ""}
    chatbot_response = process_query(user_input)

    # return appropriate response based on user selection
    if model_selction == "gpt":
        chatbot_response.pop(1) # remove llama response
    elif model_selction == "llama":
        chatbot_response.pop(0) # remove gpt response
    return jsonify(chatbot_response)

# sample process_query return
def process_query(user_input):
    time.sleep(1)
    llama_response = {
    "agentName": "medllama2",
    "agentResponse": "Ehlers-Danlos Syndrome (EDS) is a group of connective tissue disorders characterized by varying degrees of skin hyperextensibility, joint hypermobility, and tissue fragility. The syndrome encompasses multiple types, each caused by different genetic mutations affecting collagen or other components of connective tissue. Common symptoms include overly flexible joints that can dislocate easily, stretchy and fragile skin that bruises and heals poorly, and chronic pain.\n\nThe severity of EDS can range from mild to life-threatening, depending on the type. Vascular EDS, for example, can cause serious complications like ruptures of blood vessels or internal organs. Diagnosis is typically based on clinical evaluation, family history, and genetic testing. There is no cure for EDS, so treatment focuses on managing symptoms and preventing complications. This may involve physical therapy, pain management, lifestyle adjustments to avoid injury, and regular monitoring by healthcare professionals. Genetic counseling is also recommended for affected individuals and their families.",
    "urls": [
      "google.com",
      "ollama.com"
        ]
    }
    gpt_response = {
    "agentName": "gpt",
    "agentResponse": "Ehlers-Danlos Syndrome (EDS) is a group of connective tissue disorders characterized by varying degrees of skin hyperextensibility, joint hypermobility, and tissue fragility. The syndrome encompasses multiple types, each caused by different genetic mutations affecting collagen or other components of connective tissue. Common symptoms include overly flexible joints that can dislocate easily, stretchy and fragile skin that bruises and heals poorly, and chronic pain.\n\nThe severity of EDS can range from mild to life-threatening, depending on the type. Vascular EDS, for example, can cause serious complications like ruptures of blood vessels or internal organs. Diagnosis is typically based on clinical evaluation, family history, and genetic testing. There is no cure for EDS, so treatment focuses on managing symptoms and preventing complications. This may involve physical therapy, pain management, lifestyle adjustments to avoid injury, and regular monitoring by healthcare professionals. Genetic counseling is also recommended for affected individuals and their families.",
    "urls": [
      "gpt.com",
        ]
    }
    summaryString = "Here is an example summary string"
    return [gpt_response, llama_response, summaryString]

if __name__ == '__main__':
    app.run(debug=True)
