import boto3
import os
import json
ec2 = boto3.client("ec2", region_name="us-west-2",
                   aws_access_key_id=os.getenv(
                       "AWS_ACCESS_KEY_ID"),
                   aws_secret_access_key=os.getenv(
                       "AWS_SECRET_ACCESS_KEY"),
                   aws_session_token=os.getenv("AWS_SESSION_TOKEN"))
filters = [
    # {'Name': 'domain', 'Values': ['vpc']}
]
response = ec2.describe_instances(Filters=filters)
# for member in response:
#     print(member)
print(response)
