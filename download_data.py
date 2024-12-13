from azure.cosmos import CosmosClient
import pandas as pd

# Replace with your Cosmos DB credentials
url = "https://siminali.documents.azure.com:443/"
key = "LA4AlrWbFszgX5NB0sk65lmAtjv24MHAkHhCAYMvw0CVHfApnUHG3lieW2qdaJaGjVmp6qccmutmACDb31JG8Q=="
database_name = "smart_city"
container_name = "traffic_air_quality"

# Initialize the Cosmos client
client = CosmosClient(url, credential=key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Query all items in the container
items = list(container.read_all_items())

# Convert to DataFrame
df = pd.json_normalize(items)

# Save as CSV

df.to_csv("/Users/siminali/Desktop/IoT/database/cosmos_db_export.csv", index=False)


print("Data exported successfully to cosmos_db_export.csv")
