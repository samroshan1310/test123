from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME")
SECRET_NAME = "MyApiKey"

KVUri = f"https://{KEY_VAULT_NAME}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

@app.route('/')
def index():
    try:
        secret = client.get_secret(SECRET_NAME).value
    except Exception as e:
        secret = f"Error: {str(e)}"
    return f"<h1>Secret from Key Vault: {secret}</h1>"

if __name__ == '__main__':
    app.run()
