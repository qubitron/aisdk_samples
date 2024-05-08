from common.config import resource_group_name, aisearch_resource_name, location, subscription_id, credential

from azure.mgmt.search import SearchManagementClient
from azure.ai.ml import MLClient, ApiKeyConfiguration, AzureAISearchConnection

# Create AI Search resource
search_client = SearchManagementClient(
    credential=credential, subscription_id=subscription_id
)

search = search_client.services.begin_create_or_update(
    resource_group_name=resource_group_name,
    search_service_name=aisearch_resource_name,
    service={
        "location": location,
        "sku": {"name": "standard"},
        # "properties": {"hostingMode": "default", "partitionCount": 1, "replicaCount": 3},
    },
).result()

# create connection to the hub
aisearch_key = search_client.admin_keys.get(resource_group_name, aisearch_resource_name).primary_key
aisearch_endpoint = f"https://{aisearch_resource_name}.search.windows.net"

aisearch_connection = AzureAISearchConnection(
    name="azure_aisearch_connection",
    endpoint=aisearch_endpoint,
    credentials=ApiKeyConfiguration(key=aisearch_key),
)

# Create an ML client
ml_client = MLClient(workspace_name=hub_name, 
    resource_group_name=resource_group_name, 
    subscription_id=subscription_id, 
    credential=credential)

ml_client.connections.create_or_update(aisearch_connection)


