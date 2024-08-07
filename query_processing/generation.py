from langchain_core.prompts import PromptTemplate
import boto3
import json

bedrock_client = boto3.client("bedrock-runtime")
modelId = 'meta.llama3-1-70b-instruct-v1:0'
accept = 'application/json'
contentType = 'application/json'


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


    return output.get('generation')
