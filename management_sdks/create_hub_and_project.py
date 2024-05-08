from common.config import resource_group_name, hub_name, project_name, location, subscription_id, credential

# Create a resource group
from azure.mgmt.resource import ResourceManagementClient
resource_client = ResourceManagementClient(credential, subscription_id)

resource_group = resource_client.resource_groups.create_or_update(
    resource_group_name, {"location": location}
)

# Create an ML client
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
client = MLClient(workspace_name="", 
    resource_group_name=resource_group_name, 
    subscription_id=subscription_id, 
    credential=credential)

# Create a Hub
from azure.ai.ml.entities import Hub
hub_definition = Hub(name=hub_name, location=location)
print("Creating Hub, this will take a couple minutes...")
created_hub = client.workspaces.begin_create(workspace=hub_definition).result()

# Create a Project
from azure.ai.ml.entities import Project
project_definition = Project(name=project_name, hub_id=created_hub.id, location=location)
created_project = client.workspaces.begin_create(workspace=project_definition).result()
