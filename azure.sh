#!/bin/bash

# Set variables
resourceGroupName="ai-9898"
location="EastUS"
cosmosDbAccountName="qy-889"  # Must be globally unique
databaseName="MyDatabase"
# containerName="MyContainer"
partitionKey="/id"

# Create resource group
az group create \
  --name $resourceGroupName \
  --location $location

# Create Cosmos DB account with vector support
az cosmosdb create \
  --name $cosmosDbAccountName \
  --resource-group $resourceGroupName \
  --locations regionName=$location failoverPriority=0 isZoneRedundant=false \
  --default-consistency-level Session \
  --enable-free-tier true

# Enable vector search capabilities
az cosmosdb update \
  --resource-group $resourceGroupName \
  --name $cosmosDbAccountName \
  --capabilities EnableNoSQLVectorSearch

# Create the SQL database
az cosmosdb sql database create \
  --account-name $cosmosDbAccountName \
  --resource-group $resourceGroupName \
  --name $databaseName


curl -X GET "https://qy-889.documents.azure.com:443/dbs/MyDatabase/colls/bookstore" \
    -H "x-ms-date: $(date -u +'%a, %d %b %Y %H:%M:%S GMT')" \
    -H "x-ms-version: 2018-12-31" \
    -H "Authorization: aLgLfBJUBtcTe4VHL4xVPCCzzSrz4DlKKZiHqCwTxHsrUjsjI88ymY5XcA5JG4z2oiJxeiSX8Q8yACDbiLytNg==" \
    -H "Content-Type: application/json"
