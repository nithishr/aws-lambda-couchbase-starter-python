# AWS Lambda Starter using Couchbase SDK in Python

A simple starter project to get started with using the Python SDK for Couchbase in AWS Lambda environment. The lambda handlers are expecting the calls via API Gateway with the [Lambda proxy integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.htm).

## Building Docker Image

docker build -t cb-python-lambda-starter .

## Lambda Configuration

Environment variables for the lambda need to be configured on AWS

```sh
COUCHBASE_CONNECTION_STRING=<couchbase-connection-string>
COUCHBASE_USERNAME=<database-user>
COUCHBASE_PASSWORD=<database-user-password>
COUCHBASE_BUCKET=<bucket-name-in-cluster>
COUCHBASE_SCOPE=<scope-in-bucket>
COUCHBASE_COLLECTION=<collection-in-scope>
```

## Lambda Handlers

The default handler in the Docker container is set to read_document_handler. This can be overridden in the lambda configuration.

- read_document_handler(): Takes a document id in the query string and returns the document from the configured Couchbase collection.
  `?id=<document-id`
- create_document_handler(): Takes the document id & document to be inserted in the Couchbase collection in the request body.

  Sample payload

  ```json
  {
    "id": "airline_1",
    "document": {
      "id": "airline_1",
      "name": "test"
    }
  }
  ```
