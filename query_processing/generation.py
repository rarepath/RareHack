from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import openai
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

# Prompt
prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an assistant for medical question-answering tasks about two rare diseases, Hypophosphatasia and Ehler-Danlos Syndrome. 
    You have access to a database of medical documents ralated to the question they ask for context and only have the ability to answer questions based on the context provided.
    Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise <|eot_id|><|start_header_id|>user<|end_header_id|>
    Question: {question} 
    Context: {context} 
    Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "document"],
)

llm = Ollama(model="llama3:8b", temperature=0.3)


generation = prompt | llm

def generate(query, context):
    llama_response = generation.invoke({"question": query, "context": context})

    openai_response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system", 
            "content": """You are an assistant for medical question-answering tasks about two rare diseases, Hypophosphatasia and Ehler-Danlos Syndrome. 
                        You have access to a database of medical documents ralated to the question they ask for context and only have the ability to answer questions based on the context provided.
                        Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. 
                        Use three sentences maximum and keep the answer concise"""
        },
        {
            "role": "user", 
            "content": f'Question: {query} Context: {context}' }
    ],
    temperature=0.3,
    max_tokens=500
)

    gpt_response = openai_response.choices[0].message.content

    if not gpt_response:
        gpt_response = "I'm sorry, but I couldn't generate a complete response. Could you please provide more details or try asking a more specific question?"


    return {gpt_response, llama_response}




