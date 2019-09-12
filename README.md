---
page_type: sample
languages:
- python
products:
- azure
description: "This sample shows how to use the Python SDK to create, retreive, and delete Azure Container Instances."
urlFragment: container-instances-python-manage
---


# Manage Azure Container Instances 

This sample shows how to use the Python SDK to create, retreive, and delete Azure Container Instances.

## Overview

- [Getting Started](#start)
   - Install prerequisites
   - [Have an Azure security principal](#security-principal)
- [Setup The Sample](#setup)
   - Clone the repository
   - Install packages
- [Run The Sample](#run)
   - Update the placeholders
   - Execute example.py
- [Understand The Code](#example)
   - Defining an Azure execution context
   - Constructing the Azure clients
   - Execute activities

<a id="start"></a>
## Getting Started

### Install prerequisites

- **[Python installed](https://www.python.org/downloads/)**. See the [the SDK](https://github.com/Azure/azure-sdk-for-python) for supported Python versions

- A virtual environment initialized *(optional)*

   > TIP: using [virtual environments](https://docs.python.org/3/tutorial/venv.html) is recommended, but _not required_. To initialize a virtual environment, open a terminal and run the following (replace `<myvirtualenv>` in the example below with the name of your virtual environment):

    ```
    pip install virtualenv
    virtualenv <myvirtualenv>
    cd <myvirtualenv>
    source bin/activate
    ```
- [Git installed](https://git-scm.com/downloads). Download the latest client for your OS platform.

<a id="azure-principal"></a>
### Have an Azure security principal

Get or **create a security principal** to authenticate with the Azure subscription that the sample will execute against. This can be done a few ways, including:

   - the [Azure CLI 2.0](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?view=azure-cli-latest)
   - with [PowerShell](https://docs.microsoft.com/en-us/powershell/azure/create-azure-service-principal-azureps?view=azurermps-4.4.0)
   - or [using the portal](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal)


<a id="setup"></a>
## Setup The Sample

1. First, [**clone the repository**](https://help.github.com/articles/cloning-a-repository/). To do this, open a terminal, then type the following command:

    ```
    git clone https://github.com/Azure-Samples/container-instances-python-manage.git
    ```
2. Next, **install the Python packages** the sample depends on. In the same terminal window, enter the following command:

    ```
    cd container-instances-python-manage/src
    pip install -r requirements.txt
    ```

<a id="run"></a>
## Run The Sample

### Update placeholders
To run the sample, the information for the Azure security principal obtained from the [Azure security principal](#azure-principal) section must be used to update the placeholder values in the sample. 

1. First, open `example.py` and locate the following codeblock at the top of the file:

```
azure_context = AzureContext(
      subscription_id = '<SUBSCRIPTION ID>',
      client_id = '<CLIENT ID>',
      client_secret = '<CLIENT SECRET>',
      tenant = '<TENANT ID (AZURE ACTIVE DIRECTORY)>'
   )
```

2. Replace the values for `<SUBSCRIPTION ID>`, `<CLIENT ID>`, `<CLIENT SECRET>`, and `<TENANT ID (AZURE ACTIVE DIRECTORY)>`.

3. Save the changes made to `example.py`.

### Execute example.py
Using the terminal window from the previous step, or opening a new window and changing the directory to `container-instances-python-manage/src`, and type the following command:

```
python example.py
```

   > TIP: if you decided to use [virtual environnements](https://docs.python.org/3/tutorial/venv.html) as recommended, make sure the virtual environment has been activated as shown in step 3 of Getting Started above.


<a id="understand"></a>
## Understand The Code

### Define execution context

First, an Azure execution context is created with a subscription id and security principal credentials at the start of `example.py`.

```
azure_context = AzureContext(
      subscription_id = '<SUBSCRIPTION ID>',
      client_id = '<CLIENT ID>',
      client_secret = '<CLIENT SECRET>',
      tenant = '<TENANT ID (AZURE ACTIVE DIRECTORY)>'
   )
```

#### `src/utilities/azure_context.py`
This helper class is used to demonstrate **the concept** of an Azure execution context. 

   > TIP: There is no formal "execution context" object, but is conceptual. It is important to understand particularly when having to execute programs against multiple Azure subscriptions.

```
class AzureContext(object):
   def __init__(self, subscription_id, client_id, client_secret, tenant):
      self.credentials = ServicePrincipalCredentials(
         client_id = client_id,
         secret = client_secret,
         tenant = tenant
      )
      self.subscription_id = subscription_id
```

### Construct the clients
Next, the clients are constructed. This is done outside `main` method so the variables can be used in each function without having to define a client for every action.

```
resource_client = ResourceManagementClient(azure_context.credentials, azure_context.subscription_id)
client = ContainerInstanceManagementClient(azure_context.credentials, azure_context.subscription_id)
```
### Execute activities

#### `main()`

The execution steps of the code in `example.py` performs the following actions:

   - List all the container instances in the subscription
   - Define attributes of the container instance
   - Ensure the resource group is created
   - Create the container
   - Retrieve and show the newly created container instance
   - Delete and clean up

