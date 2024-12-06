from environment_utils import validate_firestore_environment, initialize_firestore_client
from json_validation_utils import load_json_file, validate_json
from logging_utils import log_error, log_success, set_logger

def populate_firestore(file_path, collection_name=None, logger=None):
   
    if logger is None:
        logger = set_logger()

    log_success(logger, "Starting Firestore population process...")

    # Validate environment and initialize Firestore client
    try:
        validate_firestore_environment(logger)
        firestore_client = initialize_firestore_client(logger)
    except ValueError as e:
        log_error(logger, "Failed to validate Firestore environment", e)
        return

    # Load JSON data
    try:
        data = load_json_file(file_path, logger)
        validate_json(data, logger)
    except (FileNotFoundError, ValueError) as e:
        log_error(logger, "Failed to load or validate JSON", e)
        raise

    # Write data to Firestore
    success_count = 0
    error_count = 0

    # Handle top-level key dynamically
    if isinstance(data, dict):
        for key, items in data.items():
            # If collection_name is specified, use it, otherwise default to the top-level key
            target_collection = collection_name or key
            if isinstance(items, list):
                for item in items:
                    doc_id = item.get("id") or generate_random_id()
                    try:
                        firestore_client.collection(target_collection).document(str(doc_id)).set(item)
                        success_count += 1
                        log_success(logger, f"Document '{doc_id}' written to collection '{target_collection}'.")
                    except Exception as e:
                        error_count += 1
                        log_error(logger, f"Failed to write document '{doc_id}' to collection '{target_collection}'", e)
            else:
                log_error(logger, f"Top-level key '{key}' does not contain a list of items.")
    elif isinstance(data, list):
        # If data is a list, use the specified collection_name or a default
        target_collection = collection_name or "default_collection"
        for item in data:
            doc_id = item.get("id") or generate_random_id()
            try:
                firestore_client.collection(target_collection).document(str(doc_id)).set(item)
                success_count += 1
                log_success(logger, f"Document '{doc_id}' written to collection '{target_collection}'.")
            except Exception as e:
                error_count += 1
                log_error(logger, f"Failed to write document '{doc_id}' to collection '{target_collection}'", e)
    else:
        log_error(logger, "Invalid JSON structure: Must be a dictionary or a list.")

    # Final summary
    log_success(logger, f"Firestore population completed: {success_count} documents written successfully.")
    if error_count > 0:
        log_error(logger, f"{error_count} documents failed to write.")

    print(f"Summary: {success_count} documents written successfully, {error_count} failed.")

    #/ utility to generate random id

    import uuid

    def generate_random_id():
        return str(uuid.uuid4())

