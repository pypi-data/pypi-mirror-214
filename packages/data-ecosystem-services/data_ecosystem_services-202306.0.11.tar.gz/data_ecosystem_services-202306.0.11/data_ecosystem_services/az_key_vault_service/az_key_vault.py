from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

class AzKeyVault:
    """Wrapper class for Azure Key Vault to get secrets.

    This class authenticates with the Azure Key Vault using a service 
    principal and provides a method to retrieve secrets.
    """    
    def __init__(self, tenant_id, client_id, client_secret, key_vault_name):
        """Initializes the KeyVaultSecrets object.
        
        Args:
            tenant_id (str): The tenant ID of your Azure account. This is the directory ID.
            client_id (str): The client ID of the service principal.
            client_secret (str): The client secret of the service principal.
            key_vault_name (str): The name of your Azure Key Vault. You can get it from the Key Vault properties in the Azure portal.
        """        

        vault_url = f"https://{key_vault_name}.vault.azure.net/"
        self.credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        self.client = SecretClient(vault_url, self.credential)

    def get_secret(self, secret_name):
        """Retrieves a secret from the Azure Key Vault.

        Args:
            secret_name (str): The name of the secret to retrieve.

        Returns:
            str: The value of the retrieved secret.
        """        
        return self.client.get_secret(secret_name).value
