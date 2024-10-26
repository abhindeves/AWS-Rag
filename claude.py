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

# Set the model ID, e.g., Claude 3 Haiku.
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

# Define the prompt for the model.
prompt = "Describe the purpose of a 'hello world' program in one line."

# Format the request payload using the model's native structure.
native_request = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 512,
    "temperature": 0.5,
    "messages": [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        }
    ],
}

# Convert the native request to JSON.
request = json.dumps(native_request)

# Invoke the model with the request.
streaming_response = client.invoke_model_with_response_stream(
    modelId=model_id, body=request
)

# Extract and print the response text in real-time.
for event in streaming_response["body"]:
    chunk = json.loads(event["chunk"]["bytes"])
    if chunk["type"] == "content_block_delta":
        print(chunk["delta"].get("text", ""), end="")

# snippet-end:[python.example_code.bedrock-runtime.InvokeModelWithResponseStream_AnthropicClaude]