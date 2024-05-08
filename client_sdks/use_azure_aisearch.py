from common.config import resource_group_name, project_name, subscription_id, credential, aisearch_index_name
from azure.ai.ml import MLClient
import os

# Use ML Client to set environment variables
ml_client = MLClient(workspace_name=project_name, 
    resource_group_name=resource_group_name, 
    subscription_id=subscription_id, 
    credential=credential)

aiservices_connection = ml_client.connections.get("azure_aisearch_connection", populate_secrets=True)
os.environ['AZURE_AISEARCH_ENDPOINT'] = aiservices_connection.target
os.environ['AZURE_AISEARCH_KEY'] = aiservices_connection.api_key
os.environ['AZURE_AISEARCH_INDEX_NAME'] = aisearch_index_name

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

index_name = os.environ["AZUREAI_SEARCH_INDEX_NAME"]
#  retrieve documents relevant to the user's question from Cognitive Search
search_client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"]),
    index_name=index_name)

aoai_client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_KEY"],    
)

# generate a vector embedding of the user's question
embedding = aoai_client.embeddings.create(input=query,
    model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"])
embedding_to_query = embedding.data[0].embedding

context = ""
# use the vector embedding to do a vector search on the index
vector_query = VectorizedQuery(vector=embedding_to_query, k_nearest_neighbors=num_docs, fields="contentVector")
results = search_client.search(
    search_text="", vector_queries=[vector_query], select=["id", "content"])

for result in results:
    context += f"\n### From: {result['id']}\n{result['content']}"


