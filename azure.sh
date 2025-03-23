
# Set variables
resourceGroupName="ai"
location="EastUS"  # Change to your preferred region
cosmosDbAccountName="MyCosmosDbAccount"  # Must be globally unique
databaseName="MyDatabase"

# az group create \
#   --name $resourceGroupName \
#   --location $location

az cosmosdb create \
  --name $cosmosDbAccountName \
  --resource-group $resourceGroupName \
  --location $location \
 --kind GlobalDocumentDB

az cosmosdb sql database create \
  --account-name $cosmosDbAccountName \
  --resource-group $resourceGroupName \
  --name $databaseName

az cosmosdb update \
  --resource-group $resourceGroupName \
  --name $cosmosDbAccountName \
  --capabilities EnableNoSQLVectorSearch
