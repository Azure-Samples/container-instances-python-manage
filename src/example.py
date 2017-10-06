from utilities import AzureContext
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (ContainerGroup, Container, ContainerPort, Port, IpAddress, 
                                                 ResourceRequirements, ResourceRequests, ContainerGroupNetworkProtocol, OperatingSystemTypes)

# See README for information on how to obtain a service principal attributes client id, secret, etc. for Azure
azure_context = AzureContext(
      subscription_id = '<SUBSCRIPTION ID>',
      client_id = '<CLIENT ID>',
      client_secret = '<CLIENT SECRET>',
      tenant = '<TENANT ID (AZURE ACTIVE DIRECTORY)>'
   )

# construct the clients
resource_client = ResourceManagementClient(azure_context.credentials, azure_context.subscription_id)
client = ContainerInstanceManagementClient(azure_context.credentials, azure_context.subscription_id)

def main():
   """Azure Container instance example."""

   # List all the container instances in the subscription
   # Define attributes of our container instance
   # ensure the resource group is created
   # Create the container
   # Retrieve and show the newly created container instance
   # delete and clean up

   list_container_groups()

   resource_group_name = "my-container-resource-group"
   name = "mycontainer"
   location = 'eastus'

   resource_client.resource_groups.create_or_update(resource_group_name, { 'location': location })

   create_container_group(resource_group_name = resource_group_name, 
                          name = name, 
                          location = location, 
                          image = "microsoft/aci-helloworld", 
                          memory = 1, 
                          cpu = 1)

   show_container_group(resource_group_name, name)

   delete_resources(resource_group_name, name)

# Utility methods

def list_container_groups():
   container_groups = client.container_groups.list()

   for container_group in container_groups:
      print("\t{0}: {{ location: '{1}', containers: {2} }}".format(
            container_group.name,
            container_group.location, 
            len(container_group.containers))
      )

def create_container_group(resource_group_name, name, location, image, memory, cpu):

   # setup default values
   port = 80
   container_resource_requirements = None
   command = None
   environment_variables = None

   # set memory and cpu
   container_resource_requests = ResourceRequests(memory_in_gb = memory, cpu = cpu)
   container_resource_requirements = ResourceRequirements(requests = container_resource_requests)
   
   container = Container(name = name,
                         image = image,
                         resources = container_resource_requirements,
                         command = command,
                         ports = [ContainerPort(port=port)],
                         environment_variables = environment_variables)

   # defaults for container group
   cgroup_os_type = OperatingSystemTypes.linux
   cgroup_ip_address = IpAddress(ports = [Port(protocol=ContainerGroupNetworkProtocol.tcp, port = port)])
   image_registry_credentials = None

   cgroup = ContainerGroup(location = location,
                           containers = [container],
                           os_type = cgroup_os_type,
                           ip_address = cgroup_ip_address,
                           image_registry_credentials = image_registry_credentials)

   client.container_groups.create_or_update(resource_group_name, name, cgroup)

def show_container_group(resource_group_name, name):
   cgroup = client.container_groups.get(resource_group_name, name)

   print('\n{0}\t\t\t{1}\t{2}'.format('name', 'location', 'provisioning state'))
   print('---------------------------------------------------')
   print('{0}\t\t{1}\t\t{2}'.format(cgroup.name, cgroup.location, cgroup.provisioning_state))

def delete_resources(resource_group_name, container_group_name): 
   client.container_groups.delete(resource_group_name, container_group_name)
   resource_client.resource_groups.delete(resource_group_name)
   
if __name__ == "__main__":
    main()