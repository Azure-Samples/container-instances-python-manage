---
services: azure-containerinstance
platforms: python
author: kevinhillinger
---

# Manage Azure Container Instances 

This sample shows how to use the Python SDK to create, retreive, and delete Azure Container Instances.

**Outline**

- [Running the sample](#run)
- [What is example.py doing?](#example)
    - [Creating the manager](#create-credentials)
      - Define a security context for connecting to Azure
         - Set the subscription ID
         - Add Client ID and Secret for specified Azure AD tenant
    - [Defining and creating the container group](#create-group)
   - [Deleting the container group](#deleting-group)
<a id="run"></a>
## Running the example

### Setting up your environment
You need to have the following installed on the development environment you will be running the sample from.

1. Install [Python](https://www.python.org/downloads/)

2. Initialize a virtual environment (optional)

   > TIP: using [virtual environnements](https://docs.python.org/3/tutorial/venv.html) is recommended, but not required. To initialize a virtual environment, run the following, replacing `<myvirtualenv> with the name you would like:

    ```
    pip install virtualenv
    virtualenv <myvirtualenv>
    cd <myvirtualenv>
    source bin/activate
    ```

3. Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/container-instances-python-manage.git
    ```

4. Install the dependencies using pip.

    ```
    cd container-instances-python-manage
    pip install -r src/requirements.txt
    ```
    
### Running the sample

Run the sample by opening a terminal window and executing the following command:

```
python src/example.py
```

<a id="example"></a>
## What is example.py doing?
