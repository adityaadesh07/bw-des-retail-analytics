import snowflake.connector
import boto3
from vaultUtil import getVaultCred

vault_url = "http://127.0.0.1:8200"
role_id = "17f4ffdd-4900-53f7-af9b-88dbee411cb2"
secret_id = "76f341dd-e1cd-87d2-c2cf-7ff83f6f88ac"
secret_path = "secret/data/snow"

# Create an instance of the getVaultCred class
vault_cred = getVaultCred(vault_url, role_id, secret_id, secret_path)

# Authenticate with AppRole and get token
token = vault_cred.authenticate_with_approle()



# Retrieve the secret using the obtained token
if token:
    # Retrieve the secret using the obtained token
    secret_data = vault_cred.get_secret(token)
    print(secret_data)

# # Extract AWS access key and secret key
# user = secret_data['data']['bw-snow-usename-dev']
# password = secret_data['data']['bw-snow-userpass-dev']

class SnowflakeConnector:
    def __init__(self, account, user, password, warehouse, database, schema):
        self.account = account
        self.user = user
        self.password = password
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = snowflake.connector.connect(
                user=self.user,
                password=self.password,
                account=self.account,
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema
            )
            self.cursor = self.connection.cursor()
            print("Connected to Snowflake successfully!")
        except Exception as e:
            print(f"Error connecting to Snowflake: {str(e)}")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            print("Query executed successfully:")
            for row in self.cursor.fetchall():
                print(row)
        except Exception as e:
            print(f"Error executing query: {str(e)}")

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")

# Example usage:
if __name__ == "__main__":
    # Replace these values with your Snowflake account information
    account_name = 'uob45577.us-east-1'
    username = secret_data['data']['bw-snow-usename-dev']
    password = secret_data['data']['bw-snow-userpass-dev']
    warehouse = 'COMPUTE_WH'
    database = 'SNOWFLAKE_SAMPLE_DATA'
    schema = 'TPCH_SF1'

    # Create an instance of the SnowflakeConnector class
    snowflake_conn = SnowflakeConnector(
        account_name, username, password, warehouse, database, schema
    )

    # Connect to Snowflake
    snowflake_conn.connect()

    # Example query
    sample_query = 'SELECT * FROM SUPPLIER'

    # Execute the query
    snowflake_conn.execute_query(sample_query)

    # Close the connection
    snowflake_conn.close_connection()
