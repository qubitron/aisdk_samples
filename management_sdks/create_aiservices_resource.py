from common.config import resource_group_name, aiservices_resource_name, location, subscription_id
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.ai.ml import MLClient, ApiKeyConfiguration, AzureAIServicesConnection

# Create AI Services resource
aiservices_client = CognitiveServicesManagementClient(
    credential=DefaultAzureCredential(), subscription_id=subscription_id
)
aiservices_account = aiservices_client.accounts.begin_create(
    resource_group_name=resource_group_name,
            account_name=aiservices_resource_name,
            account={
                "sku": {"name": "S0"},
                "kind": "AIServices",
                "location": location,
            },
        ).result()

# Create a connection to the hub
aiservices_key = aiservices_client.accounts.list_keys(
    resource_group_name=resource_group_name,
    account_name=aiservices_resource_name,
).key1

aiservices_endpoint = aiservices_client.accounts.get(
    resource_group_name=resource_group_name,
    account_name=aiservices_resource_name
).properties.endpoint

aiservices_connection = AzureAIServicesConnection(
    name="azure_aiservices_connection",
    api_key=ApiKeyConfiguration(key=aiservices_key),
    target=aiservices_endpoint,
    ai_services_resource_id=resource_id)

ml_client = MLClient(workspace_name=hub_name, 
    resource_group_name=resource_group_name, 
    subscription_id=subscription_id, 
    credential=credential)

result = ml_client.connections.create_or_update(
    connection=aiservices_connection
)


