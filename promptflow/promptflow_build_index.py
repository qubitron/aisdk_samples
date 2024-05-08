from common.config import resource_group_name, project_name, subscription_id, credential,azure_openai_embedding_model_name, aisearch_index_name
from promptflow.rag.resources import LocalSource, AzureAISearchConfig, EmbeddingsModelConfig, ConnectionConfig
from promptflow.rag import build_index

  # Use the same index name when registering the index in AI Studio
index_path = build_index(
    name=aisearch_index_name,  # name of your index
    vector_store="azure_ai_search",  # the type of vector store
    embeddings_model_config=EmbeddingsModelConfig(
        model_name=azure_openai_embedding_model_name, # the name of the model
        deployment_name=azure_openai_embedding_model_name,
        connection_config= ConnectionConfig(
            subscription=subscription_id,
            resource_group=resource_group_name,
            workspace=project_name,
            connection_name="azure_aiservices_connection"
        )
    ),
    input_source=LocalSource(input_data="./data/*.md"),  # the location of your file/folders
    index_config=AzureAISearchConfig(
            ai_search_index_name=index_name, # the name of the index store inside the azure ai search service
            ai_search_connection_config=ConnectionConfig(
            subscription=subscription_id,
            resource_group=resource_group_name,
            workspace=project_name,
            connection_name="azure_aisearch_connection"
        ) # this is so that you do not need the environment variables
    ),
    tokens_per_chunk = 800, # Optional field - Maximum number of tokens per chunk
    token_overlap_across_chunks = 0, # Optional field - Number of tokens to overlap between chunks
)

from promptflow.rag import get_langchain_retriever_from_index

# Call the index
retriever=get_langchain_retriever_from_index(ml_index.path)
retriever.get_relevant_documents("which tent is the most waterproof?")

# register the index so that it shows up in the project
from azure.ai.ml import MLClient
client.indexes.create_or_update(Index(name=index_name, path=index_path))
client = MLClient(workspace_name=project_name, 
    resource_group_name=resource_group_name, 
    subscription_id=subscription_id, 
    credential=credential)


