#!/bin/bash

# Set variables
resourceGroupName="ai-9898"
location="EastUS"
cosmosDbAccountName="qy-889"  # Must be globally unique
databaseName="MyDatabase"
containerName="MyContainer"
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
