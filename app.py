from flask import Flask, request, jsonify, render_template_string
import time
import random
import os

# Azure Key Vault libraries
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Load secret from Azure Key Vault
KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME")
SECRET_NAME = os.environ.get("SECRET_NAME", "MySecret")

KVUri = f"https://{KEY_VAULT_NAME}.vault.azure.net"

# Use managed identity (when deployed on Azure)
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

try:
    retrieved_secret = client.get_secret(SECRET_NAME)
    SECRET_VALUE = retrieved_secret.value
except Exception as e:
    SECRET_VALUE = f"Error: {str(e)}"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(f"""
        <h1>Welcome to Load Test App</h1>
        <p><a href='/form'>Form Page</a></p>
        <p><a href='/api/data'>API Endpoint</a></p>
        <p>Secret from Key Vault: <strong>{SECRET_VALUE}</strong></p>
    """)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        time.sleep(random.uniform(0.2, 1.0))
        return f"<h3>Thanks {name}, we received your data.</h3>"
    return '''
        <form method="post">
            Name: <input name="name"><br>
            Email: <input name="email"><br>
            <input type="submit">
        </form>
    '''

@app.route('/api/data')
def api_data():
    delay = random.uniform(0.1, 1.5)
    time.sleep(delay)
    return jsonify({
        "status": "success",
        "delay_seconds": round(delay, 2),
        "data": [random.randint(1, 100) for _ in range(5)],
        "secret": SECRET_VALUE
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
