import openai
import os
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

openai.api_key = os.getenv("OPENAI_API")

class ParaphrasedQuery(BaseModel):
    """You have performed query expansion to generate a paraphrasing of a question."""
    paraphrased_query: str = Field(
        ...,
        description="A unique paraphrasing of the original question.",
    )

def decorate_query(query):
    """Decorate the query by expanding any abbreviations."""
    system = """You are an expert at converting abbreviations in a user query to their full forms.\
        Remember that the abbrevations are always related to the diseases Hypophosphatasia and Ehler's Danlos syndrome.\
        Substitute the full form in the original query.
        \
        \
        Do not answer the query."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("user", f"{query}"),
        ]
    )
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

    query_abbv = prompt | llm 
    result = query_abbv.invoke(
        {
            "query": query
        }
    )
    return result.content

def get_expanded_queries(question):
    system = """You are an expert at converting user questions into database queries. \
    You have access to a database of documents about a hypophosphatasia and ehler's danlos syndrome. \
    
    Perform query expansion. If there are multiple common ways of phrasing a user question \
    or common synonyms for key words in the question, make sure to return multiple versions \
    of the query with the different phrasings.
    
    If there are acronyms or words you are not familiar with, do not try to rephrase them.
    
    If the query contains the acronyms HPP or EDS, they stand for Hypophosphatasia and \
    ehler's danlos syndrome, respectively. 
    
    You should replace all occurrences of HPP or EDS with the expanded meaning.
    
    Return at least 2 versions of the question."""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", f"{question}"),
        ]
    )
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)
    llm_with_tools = llm.bind_tools([ParaphrasedQuery])
    query_analyzer = prompt | llm_with_tools | PydanticToolsParser(tools=[ParaphrasedQuery])

    result = query_analyzer.invoke(
        {
            "question": question
        }
    )

    # Store expanded queries in a list
    expanded_queries = []
    for query in result:
        expanded_queries.append(query.paraphrased_query)

    return expanded_queries

# # Example usage:
# question = "what are the symptoms of hypophosphatasia?"
# expanded_queries = get_expanded_queries(question)

# # Print the expanded queries
# print("Expanded Queries:")
# for query in expanded_queries:
#     print(query)

# decorated_query = decorate_query("What role does TNSALP have in the body?")
# print(decorated_query)