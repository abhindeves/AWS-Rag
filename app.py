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
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

_ = load_dotenv(find_dotenv())

region = os.getenv('region')
aoss_collection_arn = os.getenv('aoss_collection_arn')
aoss_host = f"{os.path.basename(aoss_collection_arn)}.{region}.aoss.amazonaws.com"
aoss_vector_index = os.getenv('aoss_vector_index')

print(f"aoss_collection_arn={aoss_collection_arn}\naoss_host={aoss_host}\naoss_vector_index={aoss_vector_index}\naws_region={region}")


PROMPT_TEMPLATE = """Human: Answer the question based only on the information provided in few sentences.
<context>
{}
</context>
Include your answer in the <answer></answer> tags. Do not include any preamble in your answer.
<question>
{}
</question>
Assistant:"""



# create a boto3 bedrock client
bedrock_client = boto3.client('bedrock-runtime',region_name=region)

# we will use Anthropic Claude for text generation
claude_llm = ChatBedrock(model_id= "anthropic.claude-3-5-sonnet-20240620-v1:0", client=bedrock_client)

claude_llm.model_kwargs = dict(temperature=0.5, max_tokens_to_sample=300, top_k=250, top_p=1, stop_sequences=[])

# we will be using the Titan Embeddings Model to generate our Embeddings.
embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", client=bedrock_client)

# client = boto3.client('opensearchserverless')
# service = 'aoss'
# region = 'us-east-1'
# credentials = boto3.Session().get_credentials()
# awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
#                    region, service, session_token=credentials.token)


# client = OpenSearch(
#     hosts = [{'host': aoss_host, 'port': 443}],
#     http_auth = awsauth,
#     use_ssl = True,
#     verify_certs = True,
#     connection_class = RequestsHttpConnection,
#     pool_maxsize = 20
# )

bedrock_agent_runtime_client = boto3.client("bedrock-agent-runtime", region_name=region)

kb_id = 'XKHTBHXG2E'
model_arn = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0'

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

generated_text = response['output']['text']

print(generated_text)






