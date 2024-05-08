from common.config import resource_group_name, aiservices_resource_name, credential, subscription_id, \
    azure_openai_chat_model, azure_openai_embedding_model
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

client = CognitiveServicesManagementClient(
    credential=credential,
    subscription_id=subscription_id,
)

deployment = client.deployments.begin_create_or_update(
    resource_group_name=resource_group_name,
    deployment_name=azure_openai_chat_model,
    account_name=aiservices_resource_name,
    deployment={
        "properties": {
            "model": {
                "format": "OpenAI",
                "name": azure_openai_chat_model,
                "version": "0301",
            }
        },
        "sku": {"capacity": 50, "name": "Standard"},
    },
).result()

deployment = client.deployments.begin_create_or_update(
    resource_group_name=resource_group_name,
    deployment_name=azure_openai_embedding_model,
    account_name=aiservices_resource_name,
    deployment={
        "properties": {
            "model": {
                "format": "OpenAI",
                "name": azure_openai_embedding_model,
                "version": "2",
            }
        },
        "sku": {"capacity": 50, "name": "Standard"},
    },
).result()


