from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

def summarize(query, generated_response):
    # Perform your hallucination checking logic here
   
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are an advanced AI model designed to maintain conversational context. 
        Your task is to take the previous response from a chat agent and summarize it concisely. 
        This summary should capture the key points and relevant details to ensure context continuity for the next message in the conversation. 
        
        Be sure to include any specific information or instructions given by the user or the chat agent.
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        Previous Response:  {response}
        Summary: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["response"],
)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

    summarizer_chain = prompt | llm | StrOutputParser()

    summary = summarizer_chain.invoke({ "response": generated_response})

    return summary

