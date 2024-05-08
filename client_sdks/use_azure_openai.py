from common.config import resource_group_name, project_name, subscription_id, credential, azure_openai_chat_model
from azure.ai.ml import MLClient
import os

# Use ML Client to set environment variables
ml_client = MLClient(workspace_name=project_name, 
    resource_group_name=resource_group_name, 
    subscription_id=subscription_id, 
    credential=credential)

aiservices_connection = ml_client.connections.get("azure_aiservices_connection", populate_secrets=True)
os.environ['AZURE_OPENAI_ENDPOINT'] = aiservices_connection.target
os.environ['AZURE_OPENAI_KEY'] = aiservices_connection.api_key

# Call OpenAI
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT'],
  api_key=os.environ['AZURE_OPENAI_KEY'],
  api_version="2024-02-15-preview"
)

message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."},
                {"role":"user","content":"Tell me about Banco Itaú"}]

completion = client.chat.completions.create(
  model=azure_openai_chat_model, messages = message_text, 
  temperature=0.7, max_tokens=800, top_p=0.95,
  frequency_penalty=0, presence_penalty=0, stop=None
)

print(completion.choices[0].message.content)