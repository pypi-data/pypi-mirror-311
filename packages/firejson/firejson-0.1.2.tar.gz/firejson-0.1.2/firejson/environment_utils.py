import os
from google.cloud import firestore

def validate_firestore_environment(logger=None):
   
    # Validate the GOOGLE_APPLICATION_CREDENTIALS environment variable
    env_var = "GOOGLE_APPLICATION_CREDENTIALS"
    if env_var not in os.environ:
        raise ValueError(f"Environment variable '{env_var}' is not set. Please set it to the path of your service account key file.")

    credentials_path = os.environ[env_var]
    if not os.path.exists(credentials_path):
        raise ValueError(f"The file specified in '{env_var}' does not exist: {credentials_path}")

    print(f"Environment variable '{env_var}' is set and valid.")


def initialize_firestore_client(logger=None):
   
    try:
        client = firestore.Client()
        print("Firestore client authenticated successfully!")
        return client
    except Exception as e:
        raise ValueError(f"Failed to initialize Firestore client: {e}")
    

def list_firestore_collections(client):
    try:
        collections = client.collections()
        collection_names = [collection.id for collection in collections]
        print("Available collections in firestore:")
        for name in collection_names:
            print(f"-{name}")
        return collection_names
    except Exception as e:
        raise ValueError(f"Failed to list Firestore collections: {e}")