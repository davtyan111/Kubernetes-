import base64
import json
import boto3
from kubernetes import client, config

# Получаем доступ к AWS Secrets Manager
secrets_manager = boto3.client('secretsmanager', region_name='us-east-2')

# Получаем секрет из AWS Secrets Manager
secret_name = 'my-secrets'
response = secrets_manager.get_secret_value(SecretId=secret_name)
secret_value = json.loads(response['SecretString'])

# Конфигурируем доступ к кластеру Kubernetes
config.load_kube_config()

# Создаем объект клиента Kubernetes
kubernetes_client = client.CoreV1Api()

# Создаем пустой словарь для секретных данных
secret_data = {}

# Заполняем словарь секретными данными
for key, value in secret_value.items():
    secret_data[key] = base64.b64encode(value.encode()).decode()

# Создаем секрет Kubernetes
metadata = {'name': 'api-token'}
secret = client.V1Secret(data=secret_data, metadata=metadata)

# Создаем или обновляем секрет в Kubernetes
namespace = 'production'
try:
    kubernetes_client.create_namespaced_secret(namespace=namespace, body=secret)
    print(f"Секрет {secret.metadata.name} успешно создан в пространстве имен {namespace}.")
except client.exceptions.ApiException as e:
    if e.status == 409:
        try:
            kubernetes_client.replace_namespaced_secret(name=secret.metadata['name'], namespace=namespace, body=secret)
            print(f"Секрет {secret.metadata['name']} успешно обновлен в пространстве имен {namespace}.")
        except client.exceptions.ApiException as e:
            print(f"Ошибка при обновлении секрета: {e}")
    else:
        print(f"Ошибка при создании/обновлении секрета: {e}")
