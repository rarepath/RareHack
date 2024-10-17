from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import openai
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from transformers import AutoModelForCausalLM, AutoTokenizer, QuantoConfig
from query_processing.model_config import model_name
import boto3
import json

bedrock_client = boto3.client("bedrock-runtime")
modelId = 'meta.llama3-1-70b-instruct-v1:0'
accept = 'application/json'
contentType = 'application/json'


# quantization_config = QuantoConfig(weights="float8")

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(
#                                              model_name, 
#                                              pad_token_id=tokenizer.eos_token_id,
#                                              device_map = "auto", 
#                                              trust_remote_code=True, 
#                                              quantization_config=quantization_config                                
#                                              )



# def get_formatted_input(messages, context):
#     system = """System: You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
#         You will be given relevant context to answer user queries.
#         Answer the user query only using the given context and ensure your response is accurate, clear, and concise.
#         Do not mention in your response that you were given context."""
#     instruction = "Please give a full and complete answer for the question."

#     for item in messages:
#         if item['role'] == "user":
#             ## only apply this instruction for the first user turn
#             item['content'] = instruction + " " + item['content']
#             break

#     conversation = '\n\n'.join(["User: " + item["content"] if item["role"] == "user" else "Assistant: " + item["content"] for item in messages]) + "\n\nAssistant:"
#     formatted_input = system + "\n\n" + str(context) + "\n\n" + conversation
    
#     return formatted_input




def generate_llama(query, context, summary):

    if summary == "":
        llama_prompt = PromptTemplate(
            template="""System: You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
            You will be given relevant context to answer user queries. 
            Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
            Do not mention in your response that you were given context. If the question is unrelated to Hypophosphatasia or Ehlers-Danlos Syndrome. Refuse to answer.
            
            User: Question: {question} 
            Context: {context}
            Assistant:""",
        input_variables=["question", "context"],
        )
    else:
        llama_prompt = PromptTemplate(
            template="""System: You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
            You will be given relevant context to answer user queries. The user will provide you with a summary of the last response you generated.
            Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
            Do not mention in your response that you were given context. If the question is unrelated to Hypophosphatasia or Ehlers-Danlos Syndrome. Refuse to answer.
            
            User: Question: {question} 
            Summary: {summary}
            Context: {context}
            Assistant:""",
        input_variables=["question", "context", "summary"],
        )


    formatted_input = llama_prompt.format(question=query, context=context, summary=summary)

    body = json.dumps({
        "prompt": formatted_input,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    response = bedrock_client.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    output = json.loads(response.get('body').read())

# text

    return output.get('generation')


def generate_gpt(query, context, summary):
    if summary == "":
        messages = [
                {
                    "role": "system", 
                    "content": """You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
                    You will be given relevant context to answer user queries. 
                    Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
                    Do not mention in your response that you were given context. If the question is unrelated to Hypophosphatasia or Ehlers-Danlos Syndrome. Refuse to answer."""
                },
                {
                    "role": "user", 
                    "content": f'''Question: {query} Context: {context}'''
                }
            ]
    else:
        messages = [
                {
                    "role": "system", 
                    "content": """You are an expert in Question and Answering tasks specifically regarding rare diseases, focusing on Hypophosphatasia and Ehlers-Danlos Syndrome. 
                    You will be given relevant context to answer user queries. The user will provide you with a summary of the last response you generated.
                    Answer the user query only using the given context and ensure your response is accurate, clear, and concise. 
                    Do not mention in your response that you were given context. Say you do not know the answer if the question is unrelated to Hypophosphatasia or Ehlers-Danlos Syndrome."""
                },
                {
                    "role": "user", 
                    "content": f'''Summary: {summary} Question: {query} 
                    Context: {context} '''
                }
            ]
    

    try:
        openai_response = openai.chat.completions.create(
        model="gpt-4o",
        messages= messages,
        temperature=0.3,
        max_tokens=250

        )

        gpt_response = openai_response.choices[0].message.content

    except Exception as e:
        print("Error generating response: ", e)
        gpt_response = "Encountered an error while generating response. Please try again later."

    return gpt_response
