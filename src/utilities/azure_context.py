from azure.common.credentials import ServicePrincipalCredentials


class AzureContext(object):
    """Azure Security Context. 

       remarks:
       This is a helper to combine service principal credentials with the subscription id.
       See README for information on how to obtain a service principal attributes client id, secret, etc. for Azure
    """

    def __init__(self, subscription_id, client_id, client_secret, tenant):
        self.credentials = ServicePrincipalCredentials(
            client_id=client_id,
            secret=client_secret,
            tenant=tenant
        )
        self.subscription_id = subscription_id
