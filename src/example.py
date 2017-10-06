from haikunator import Haikunator
from utilities import AzureContext
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (ContainerGroup, Container, ContainerPort, Port, IpAddress, 
                                                 ResourceRequirements, ResourceRequests, ContainerGroupNetworkProtocol, OperatingSystemTypes)

# TODO: document this

haikunator = Haikunator()

# azure_context = AzureContext(
#       subscription_id = '<SUBSCRIPTION ID>',
#       client_id = '<CLIENT ID>',
#       client_secret = '<CLIENT SECRET>',
#       tenant = '<TENANT ID (AZURE ACTIVE DIRECTORY)>'
#    )

azure_context = AzureContext(
      subscription_id = '6c5159d3-e9b1-4eaf-b961-7d8c4717390a',
      client_id = 'e6623e02-bceb-4499-bc4e-db4c47e44590',
      client_secret = 'X38o+W0ZxV1iweEfdCWHa/QzQ+ghXNa3nCUWp0MZSzI=',
      tenant = '72f988bf-86f1-41af-91ab-2d7cd011db47'
   )
client = ContainerInstanceManagementClient(azure_context.credentials, azure_context.subscription_id)

def main():
   """Azure Container instance example."""

   # List all the container instances in the subscription
   # Define attributes of our container instance
   # ensure the resource group is created
   # Create the container
   # Get the newly created container instance
   # delete and clean up

   list_container_groups()

   resource_group_name = "my-container-resource-group"
   name = "mycontainer"
   location = 'eastus'
   image = "microsoft/aci-helloworld"
   cpu = 1
   memory = 1
   
   create_resource_group(resource_group_name, location)

   create_container_group(resource_group_name, name, location, image, memory, cpu)
   
   show_container_group(resource_group_name, name)

   client.container_groups.delete(resource_group_name, name)

def create_resource_group(name, location):
      resource_client = ResourceManagementClient(azure_context.credentials, azure_context.subscription_id)
      resource_group = resource_client.resource_groups.create_or_update(name, { 'location': location })

def create_container_group(resource_group_name, name, location, image, memory, cpu):

   # setup default values
   port = 80
   container_resource_requirements = None
   command = None
   command_line = None
   environment_variables = None
   registry_login_server = None
   registry_username = None
   registry_password = None

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

def list_container_groups():
   container_groups = client.container_groups.list()

   for container_group in container_groups:
      print("\t{0}: {{ location: '{1}', containers: {2} }}".format(
            container_group.name,
            container_group.location, 
            len(container_group.containers))
      )

def show_container_group(resource_group_name, name):
   cg = client.container_groups.get(resource_group_name, name)

   print('\n{0}\t\t\t{1}\t{2}'.format('name', 'location', 'provisioning state'))
   print('---------------------------------------------------')
   print('{0}\t\t{1}\t\t{2}'.format(cg.name, cg.location, cg.provisioning_state))


if __name__ == "__main__":
    main()