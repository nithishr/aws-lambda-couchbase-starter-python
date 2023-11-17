from datetime import timedelta
import os
import json

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions

# creating global connection objects for sharing across requests
cluster, bucket, collection = None, None, None


def get_collection():
    """Returns collection objects. Creates connection to cluster if the connection is not already established"""
    global cluster, bucket, collection
    if not collection:
        # Read environment variables
        conn_str = os.getenv("COUCHBASE_CONNECTION_STRING")
        db_username = os.getenv("COUCHBASE_USERNAME")
        db_password = os.getenv("COUCHBASE_PASSWORD")
        bucket_name = os.getenv("COUCHBASE_BUCKET")
        scope_name = os.getenv("COUCHBASE_SCOPE")
        collection_name = os.getenv("COUCHBASE_COLLECTION")

        # Connect options - authentication
        auth = PasswordAuthenticator(db_username, db_password)

        # get a reference to our cluster
        options = ClusterOptions(auth)

        # Sets a pre-configured profile called "wan_development" to help avoid latency issues
        # when accessing Capella from a different Wide Area Network
        # or Availability Zone(e.g. your laptop).
        options.apply_profile("wan_development")

        cluster = Cluster(conn_str, options)

        # Wait until the cluster is ready for use.
        cluster.wait_until_ready(timedelta(seconds=5))

        # get a reference to our bucket
        bucket = cluster.bucket(bucket_name)

        collection = bucket.scope(scope_name).collection(collection_name)

    return collection


def read_document_handler(event, context):
    """Handler to read a document from the collection"""
    response = {"statusCode": 200}
    error = None
    result = None

    try:
        # read & validate document_id from event
        try:
            document_id = event["queryStringParameters"].get("id")
        except KeyError:
            error = {"error": "Please provide an id in the query parameters"}
        else:
            collection = get_collection()
            document = collection.get(document_id).content_as[str]
            result = {"document": document}
    except Exception as e:
        error = {"error": str(e)}

    if error:
        response["statusCode"] = 400
        response["body"] = json.dumps(error)
    else:
        response["body"] = json.dumps(result)
    return response


def create_document_handler(event, context):
    """Handler to insert a document in the collection"""
    response = {"statusCode": 201}
    error = None
    result = None

    try:
        # read  & validate payload from event
        try:
            payload = json.loads(event["body"])
            document_id = payload.get("id", "")
            document = payload.get("document", "")
            if not document_id:
                error = {"error": "Please provide an id in the request"}
            if not document:
                error = {"error": "Please provide a document to insert in the request"}
        except TypeError:
            error = {"error": "Please provide an id and document in the request body"}

        if not error:
            collection = get_collection()
            res = collection.insert(document_id, document)
            result = {"cas": res.cas}
    except Exception as e:
        error = {"error": str(e)}

    if error:
        response["statusCode"] = 400
        response["body"] = json.dumps(error)
    else:
        response["body"] = json.dumps(result)
    return response
