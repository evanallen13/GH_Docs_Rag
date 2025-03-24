#!/bin/bash

# Set variables
resourceGroupName="ai-46546"
location="EastUS"
cosmosDbAccountName="qy-111"  # Must be globally unique
databaseName="MyDatabase"
containerName="MyContainer"
partitionKey="/id"

# # Create resource group
# az group create \
#   --name $resourceGroupName \
#   --location $location

# # Create Cosmos DB account with vector support
# az cosmosdb create \
#   --name $cosmosDbAccountName \
#   --resource-group $resourceGroupName \
#   --locations regionName=$location failoverPriority=0 isZoneRedundant=false \
#   --kind GlobalDocumentDB \
#   --default-consistency-level Session \
#   --enable-free-tier true

# # Enable vector search capabilities
# az cosmosdb update \
#   --resource-group $resourceGroupName \
#   --name $cosmosDbAccountName \
#   --capabilities EnableNoSQLVectorSearch

# # Create the SQL database
# az cosmosdb sql database create \
#   --account-name $cosmosDbAccountName \
#   --resource-group $resourceGroupName \
#   --name $databaseName

# Define the indexing policy (as JSON)
indexingPolicy=$(cat <<EOF
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    {
      "path": "/*"
    }
  ],
  "excludedPaths": [
    {
      "path": "/\"_etag\"/?"
    },
    {
      "path": "/coverImageVector/*"
    }
  ],
  "fullTextIndexes": []
}
EOF
)

# Define the vector embeddings policy
vectorEmbeddingPolicy=$(cat <<EOF
{
  "vectorEmbeddings": [
    {
      "path": "/coverImageVector/*",
      "dataType": "float32",
      "distanceFunction": "dotproduct",
      "dimensions": 8
    }
  ]
}
EOF
)

# Create container with custom indexing and vector embedding
az cosmosdb sql container create \
  --account-name $cosmosDbAccountName \
  --resource-group $resourceGroupName \
  --database-name $databaseName \
  --name $containerName \
  --partition-key-path $partitionKey \
  --idx "$indexingPolicy" 