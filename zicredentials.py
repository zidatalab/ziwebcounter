# Configure Access to Credentials, need to be accessed by API
# This tries to get a token using Azure MSI for devtesting a fallback to SP env variables is integrated
# FOR TESTING: Make sure to set DEVTESTSECRET in Terminal before run. i.e. EXPORT DEVTESTSECRET my_example_secret_key

from msrestazure.azure_active_directory import ServicePrincipalCredentials, MSIAuthentication
from azure.keyvault import KeyVaultClient
import os


def zicredentials():
    # check if running on azure
    if "WEBSITE_SITE_NAME" in os.environ:
        return MSIAuthentication()
    # if running locally
    else:
        # try if secrets are provided, else return none
        try:
            APPCLIENT = os.environ['APPCLIENTID']
            DEVTESTSECRET = os.environ['DEVTESTSECRET']
            TENANT = os.environ['TENANT']
            return ServicePrincipalCredentials(
                client_id=APPCLIENT,
                secret=DEVTESTSECRET,
                tenant=TENANT  # Our Azure AD ID
                )
        except Exception:
            return None


def get_zi_secret(name_of_secret):
    VAULTID = "https://zivmkeyvault.vault.azure.net"  # Our Azure Keyvault ID where App needs to be registered
    # Try to use credentials to get latest version of secret
    try:
        credentials = zicredentials()
        key_vault_client = KeyVaultClient(credentials)
        secret = key_vault_client.get_secret(VAULTID, name_of_secret, "")
        return secret.value
    except Exception:
        return None
