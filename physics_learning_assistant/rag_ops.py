from ollama import chat
from qdrant_client import QdrantClient
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

QDRANT_URL = "------------->> provide your url <<-------------"
QDRANT_TOKEN = "------------->> provide your token <<-------------"


def qdrant_connection():
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_TOKEN
    )
    return qdrant_client

def hybrid_qdrant_query(embedded_query):
    print('RETRIEVING DATA FROM QDRANT')
    qd = qdrant_connection()
    hits = qd.search(
        collection_name="physics_data",
        query_vector=embedded_query,
        limit=15
    )
    return hits

def get_query_embedding(query):
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")
    embeddings = embed_model.get_text_embedding(query)
    return embeddings

def create_prompt(query, response):
    return f'''
<CONTENT_BEGIN>
{response}
<CONTENT_END>
<USER_QUERY_START>
{query}
<USER_QUERY_END>
'''


def llm_response(user_query: str) -> str:
    try:
        print("STARTED")
        print("EMBEDDING THE QUERY")
        embedded_query = get_query_embedding(user_query)
        print("QUERY IS EMBEDDED")
        qdrant_response = hybrid_qdrant_query(embedded_query)
        print(f"DATA IS FETCHED")
        print("CREATING PROMPT")
        prompt = create_prompt(query=user_query, response=qdrant_response)
        print("PROMPT CREATED")
        messages = [{
            "role": "system",
            "content": "You are a tutor, teacher or professor who is teaching Physics, Chemistry or Biology" 
                        "Your users are students who are preparing for their NEET medical entrance exam in India"
                        "Your goal is to solve their doubts, explain specified topics or concepts, help them in derivation of formulaes, solve their numercial problems or create quetion paper for them based on the difficulty level they ask"
                        "You need to provide answer to the USER_QUERY based on the CONTENT provided",
            "content": prompt
        }]
        model = "llama3"
        
        print("LLM WORKING...")
        response = chat(
            model=model,
            messages=messages,
        )
        print("RESPONSE GENERATED")
        print()
        return response['message']['content']
    
    except Exception as e:
        print(f"An error occurred while generating the response: {e}")
        return "I'm sorry, but I couldn't generate a response at this time. Please try again later."

# # Example usage
# if __name__ == "__main__":
#     query = "What is the capital of France?"
#     response = llm_response(query)
#     print(f"Query: {query}")
#     print(f"Response: {response}")