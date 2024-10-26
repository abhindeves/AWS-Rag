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


s3_resource = boto3.resource("s3")
print("Hello, Amazon S3! Let's list your buckets:")
for bucket in s3_resource.buckets.all():
    print(f"\t{bucket.name}")