import os
import sys
import json
import boto3
from typing import Dict
from dotenv import load_dotenv, find_dotenv
from urllib.request import urlretrieve

_ = load_dotenv(find_dotenv())

region = os.getenv('region')
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')

kb_id = os.getenv('kb_id')
model_arn = os.getenv('model_arn')

bedrock_agent_runtime_client = boto3.client(
    "bedrock-agent-runtime", region_name='us-east-1',aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

response = bedrock_agent_runtime_client.retrieve_and_generate(
    input={
        'text': 'what is the milage of ecoDrive?'
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration':{
            'knowledgeBaseId':kb_id,
            'modelArn': model_arn
            
        }
    }
    
)

# generated_text = response['output']['text']

print(response)