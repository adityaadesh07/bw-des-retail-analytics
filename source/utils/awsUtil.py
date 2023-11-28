import boto3
from vaultUtil import getVaultCred

vault_url = "http://127.0.0.1:8200"
role_id = "6d0a8404-231f-380a-b175-0e6ecacd6c89"
secret_id = "7a232f6f-d00e-564b-546b-5f7d9723dc0e"
secret_path = "secret/data/aws"

# Create an instance of the getVaultCred class
vault_cred = getVaultCred(vault_url, role_id, secret_id, secret_path)

# Authenticate with AppRole and get token
token = vault_cred.authenticate_with_approle()



# Retrieve the secret using the obtained token
if token:
    # Retrieve the secret using the obtained token
    secret_data = vault_cred.get_secret(token)
    print(secret_data)

    # Extract AWS access key and secret key
    aws_access_key = secret_data['data']['bw-aws-accesskey-dev']
    aws_secret_key = secret_data['data']['bw-aws-secretkey-dev']   
    aws_region = "us-east-1"

    session = boto3.Session(aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_key,
                            region_name=aws_region)

    # Connect to AWS
    # aws_session = connect_to_aws(aws_access_key, aws_secret_key, aws_region)

    # Example: List all S3 buckets in the account
    s3_client = session.client("s3")
    response = s3_client.list_buckets()

    print("S3 Buckets:")
    for bucket in response["Buckets"]:
        print(f"- {bucket['Name']}")