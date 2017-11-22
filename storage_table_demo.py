import string
import random
import time
import json
import azurerm

from azure.storage.table import TableService, Entity

# Define variables to handle Azure authentication
auth_token = azurerm.get_access_token_from_cli()
subscription_id = azurerm.get_subscription_from_cli()

# Define variables with random resource group and storage account names
resourcegroup_name = 'RG1'
#'NS'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
storageaccount_name = 'nikistorage11202017'
#'NS'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
#location = 'eastus'

###
# Create the a resource group for our demo
# We need a resource group and a storage account. A random name is generated, as each storage account name must be globally unique.
###
# response = azurerm.create_resource_group(
#   auth_token, subscription_id, resourcegroup_name, location)
# if response.status_code == 200 or response.status_code == 201:
#    print('Resource group: ' + resourcegroup_name + ' created successfully.')
# else:
#    print('Error creating resource group')

# Create a storage account for our demo
#response = azurerm.create_storage_account(auth_token, subscription_id, resourcegroup_name, storageaccount_name,  location, storage_type='Standard_LRS')
#if response.status_code == 202:
#    print('Storage account: ' + storageaccount_name + ' created successfully.')
#    time.sleep(2)
#else:
#    print('Error creating storage account')


###
# Use the Azure Storage Storage SDK for Python to create a Table
print('\nLet\'s create an Azure Storage Table to store some data.')
raw_input('Press Enter to continue...')

# Each storage account has a primary and secondary access key.
# These keys are used by applications to access data in your storage account, such as Tables.
# Obtain the primary storage access key for use with the rest of the demo

response = azurerm.get_storage_account_keys(auth_token, subscription_id, resourcegroup_name, storageaccount_name)
storageaccount_keys = json.loads(response.text)
#storageaccount_primarykey = storageaccount_keys['keys'][0]['value']

# Create the Table with the Azure Storage SDK and the access key obtained in the previous step
table_service = TableService(
    account_name=storageaccount_name, account_key='Bk5ar/6mKz/74JvgLNnw6obZEkL6Jnsy2TuR4wc8qY/YX/N66xvNjRMuU+BTNr5pW579DaymVhKN/4s3urewFg==')
response = table_service.create_table('itemstable2')
if response == True:
    print('Storage Table: itemstable2 created successfully.\n')
else:
    print('Error creating Storage Table.\n')

time.sleep(1)


###
# Use the Azure Storage Storage SDK for Python to create some entries in the Table
###
print('Now let\'s add some entries to our Table.\nRemember, Azure Storage Tables is a NoSQL datastore, so this is similar to adding records to a database.')
raw_input('Press Enter to continue...')
# Each entry in a Table is called an 'Entity'. 
# Here, we add an entry for first cars with two pieces of data - the name, and the cost
# A partition key tracks how like-minded entries in the Table are created and queried.
# A row key is a unique ID for each entity in the partition
# These two properties are used as a primary key to index the Table. This makes queries much quicker.

cars = Entity()
cars.PartitionKey = 'cardealership'
cars.RowKey = '001'
cars.make = 'Mitsubishi'
cars.model = 'Galant'
cars.year = 2002
cars.color = 'Silver'
cars.price = 2400
table_service.insert_entity('itemstable2', cars)
print('Created entry for Mitsubishi...')

cars = Entity()
cars.PartitionKey = 'cardealership'
cars.RowKey = '002'
cars.make = 'Honda'
cars.model = 'Civic'
cars.year = 2013
cars.color = 'Charcoal'
cars.price = 14000
table_service.insert_entity('itemstable2', cars)
print('Created entry for Honda...')

# A partition key tracks how like-minded entries in the Table are created and queried.
# A row key is a unique ID for each entity in the partition
# These two properties are used as a primary key to index the Table. 
# This makes queries much quicker.
coffee = Entity()
coffee.PartitionKey = 'coffeeshop'
coffee.RowKey = '003'
coffee.brand = 'Starbucks'
coffee.flavor = 'French Roast'
#Being conscious of those with dairy-free diets-- add an extra $1
coffee.milktype = 'Soy or almond'
coffee.size = 'Small'
coffee.price = 4.50
table_service.insert_entity('itemstable2', coffee)
print('Created entry for Starbucks...\n')
time.sleep(1)

coffee = Entity()
coffee.PartitionKey = 'coffeeshop'
coffee.RowKey = '004'
coffee.brand = 'Peets Coffee'
coffee.flavor = 'Costa Rica Aurora'
#Being conscious of those with dairy-free diets-- add an extra $1
coffee.milktype = 'Soy or almond'
coffee.size = 'Small'
coffee.price = 4.50
table_service.insert_entity('itemstable2', coffee)
print('Created entry for Peets Coffee...\n')
time.sleep(1)

###
# Use the Azure Storage Storage SDK for Python to query for entities in our Table
###
print('With some data in our Azure Storage Table, we can query the data.\nLet\'s see what the cars menu looks like.')
raw_input('Press Enter to continue...')
# In this query, you define the partition key to search within, and then which properties to retrieve
# Structuring queries like this improves performance as your application scales up and keeps the queries efficient
items = table_service.query_entities('itemstable2', filter="PartitionKey eq 'cardealership'", select='make,model,year,color,price')
for item in items:
    print('Make: ' + item.make)
    print('Price: ' + str(item.price) + '\n')

items = table_service.query_entities('itemstable2', filter="PartitionKey eq 'coffeeshop'", select='brand,flavor,milktype,size,price')
for item in items:
    print('Brand: ' + item.brand)
    print('Price: ' + str(item.price) + '\n')

time.sleep(1)

# This was a quick demo to see Tables in action.
# Although the actual cost is minimal (fractions of a cent per month) 
# for the three entities we created, it's good to clean up resources when you're done.

print('\nThis is a basic example of how Azure Storage Tables behave like a database.\nTo keep things tidy, let\'s clean up the Azure Storage resources we created.')
raw_input('Press Enter to continue...')

response = table_service.delete_table('itemstable2')
if response == True:
    print('Storage table: itemstable2 deleted successfully.')
else:
    print('Error deleting Storage Table')

#response = azurerm.delete_resource_group(
#    auth_token, subscription_id, resourcegroup_name)
#if response.status_code == 202:
#    print('Resource group: ' + resourcegroup_name + ' deleted successfully.')
#else:
#    print('Error deleting resource group.')
