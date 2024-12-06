import os
import json
from logging_utils import log_success, log_error


def validate_file_path(file_path, logger=None):
   
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        if not file_path.endswith(".json"):
            raise ValueError(f"The file '{file_path}' is not a JSON file.")

        if logger:
            log_success(logger, f"File '{file_path}' validated successfully!")
    except Exception as e:
        if logger:
            log_error(logger, f"File validation failed for '{file_path}'", e)
        raise


def load_json_file(file_path, logger=None):
   
    # Validate the file path first
    validate_file_path(file_path, logger)

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        if logger:
            log_success(logger, f"JSON file '{file_path}' loaded successfully!")
        return data
    except json.JSONDecodeError as e:
        if logger:
            log_error(logger, f"Invalid JSON format in file '{file_path}'", e)
        raise ValueError(f"Invalid JSON format in file '{file_path}': {e}")


def validate_json_structure(data, logger=None):
   
    try:
        if not isinstance(data, (list, dict)):
            raise ValueError("Invalid JSON structure: JSON must be a list of objects or a single object.")

        if isinstance(data, dict):
            data = [data]

        for item in data:
            if not isinstance(item, dict):
                raise ValueError(f"Invalid JSON structure: Each item must be a dictionary. Found: {type(item)}")

        if logger:
            log_success(logger, "JSON structure validated successfully!")
    except Exception as e:
        if logger:
            log_error(logger, "JSON structure validation failed", e)
        raise


def validate_firestore_keys(data, logger=None):
   
    try:
        invalid_chars = ["~", "*", "/", "[", "]"]
        if isinstance(data, dict):
            data = [data]

        for item in data:
            for key in item.keys():
                if any(char in key for char in invalid_chars):
                    raise ValueError(f"Invalid key '{key}': Keys cannot contain {invalid_chars}")

        if logger:
            log_success(logger, "Firestore keys validated successfully!")
    except Exception as e:
        if logger:
            log_error(logger, "Firestore key validation failed", e)
        raise


def validate_no_nested_collections(data, logger=None):
    """
    Validates that there are no nested structures in the JSON.

    Args:
        data (list or dict): Parsed JSON data.
        logger (logging.Logger, optional): Logger instance for logging.

    Raises:
        ValueError: If nested collections are found.
    """
    try:
        # If the data is a dictionary, treat it as a top-level JSON object
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    # Validate each item in the list
                    for item in value:
                        if isinstance(item, dict):
                            for sub_key, sub_value in item.items():
                                if isinstance(sub_value, (list, dict)):
                                    raise ValueError(f"Nested structure detected in key '{sub_key}': {sub_value}")
                elif isinstance(value, dict):
                    raise ValueError(f"Unexpected nested dictionary under key '{key}': {value}")
        elif isinstance(data, list):
            # If the data is a list, validate each item
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, (list, dict)):
                            raise ValueError(f"Nested structure detected in key '{key}': {value}")
        else:
            raise ValueError(f"Invalid JSON structure: Expected dict or list, got {type(data)}.")

        if logger:
            log_success(logger, "No nested collections found in JSON!")
    except Exception as e:
        if logger:
            log_error(logger, "Nested collection validation failed", e)
        raise


def validate_json(data, logger=None):
   
    try:
        validate_json_structure(data, logger)
        validate_firestore_keys(data, logger)
        validate_no_nested_collections(data, logger)
        if logger:
            log_success(logger, "JSON validated successfully for Firestore!")
    except Exception as e:
        if logger:
            log_error(logger, "JSON validation failed", e)
        raise