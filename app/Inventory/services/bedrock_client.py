import boto3


def get_bedrock_client():

    client = boto3.client(
        service_name="bedrock-runtime",
        region_name="eu-north-1"
    )

    return client