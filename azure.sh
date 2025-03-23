#!/bin/bash
# Set variables
resourceGroupName="ai-46546"
location="EastUS"  # Change to your preferred region
cosmosDbAccountName="qy-424324"  # Must be globally unique
databaseName="MyDatabase"

az group create \
  --name $resourceGroupName \
  --location $location

az cosmosdb create \
  --name $cosmosDbAccountName \
  --resource-group $resourceGroupName \
  --locations regionName=$location failoverPriority=0 isZoneRedundant=false \
  --kind GlobalDocumentDB \
  --default-consistency-level Session \
  --enable-free-tier true

az cosmosdb sql database create \
  --account-name $cosmosDbAccountName \
  --resource-group $resourceGroupName \
  --name $databaseName

az cosmosdb update \
  --resource-group $resourceGroupName \
  --name $cosmosDbAccountName \
  --capabilities EnableNoSQLVectorSearch