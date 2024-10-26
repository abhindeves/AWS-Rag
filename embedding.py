import os
import sys
import json
import boto3
from typing import Dict
from dotenv import load_dotenv, find_dotenv
from urllib.request import urlretrieve
from langchain_aws import ChatBedrock
from langchain_aws import BedrockEmbeddings
from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

_ = load_dotenv(find_dotenv())


region = os.getenv('region')
aoss_collection_arn = os.getenv('aoss_collection_arn')
aoss_host = f"{os.path.basename(aoss_collection_arn)}.{region}.aoss.amazonaws.com"
aoss_vector_index = os.getenv('aoss_vector_index')

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')

print(f"aoss_collection_arn={aoss_collection_arn}\naoss_host={aoss_host}\naoss_vector_index={aoss_vector_index}\naws_region={region}\naws_access_key_id={aws_access_key_id}\naws_secret_access_key={aws_secret_access_key}")


# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name=region)

# Set the model ID, e.g., Titan Text Embeddings V2.
model_id = "amazon.titan-embed-text-v2:0"

# The text to convert to an embedding.
input_text = "Please recommend books with a theme similar to the movie 'Inception'."

# Create the request for the model.
native_request = {"inputText": input_text}

# Convert the native request to JSON.
request = json.dumps(native_request)

# Invoke the model with the request.
response = client.invoke_model(modelId=model_id, body=request)

# Decode the model's native response body.
model_response = json.loads(response["body"].read())

# Extract and print the generated embedding and the input text token count.
embedding = model_response["embedding"]
input_token_count = model_response["inputTextTokenCount"]

print("\nYour input:")
print(input_text)
print(f"Number of input tokens: {input_token_count}")
print(f"Size of the generated embedding: {len(embedding)}")
print("Embedding:")
print(embedding)

# snippet-end:[python.example_code.bedrock-runtime.InvokeModel_TitanTextEmbeddings]