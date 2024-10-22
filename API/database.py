from azure.cosmos import CosmosClient, exceptions, PartitionKey

COSMOS_ENDPOINT = 'https://azcdb-dam.documents.azure.com:443/'
COSMOS_KEY = '0EgYze9fkgOGddU8AnolzDrgC7RuGy8LdK4v8By8h6Pk3y39axqaQ2wI0LmWw79lXnVh67En9AhEACDbi8iLzg=='

DATABASE_NAME = 'test_db'
CONTAINER_NAME = 'retail'

#Inicializa cliente de cosmos
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

#Crea u obtiene la bd
database = client.create_database_if_not_exists(id=DATABASE_NAME)

#Crea u obtiene el container
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path='/categoria'),
    offer_throughput=400
    )