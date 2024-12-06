---

FireJSON

A Python library for validating JSON files and populating them into Google Firestore collections.


---

Installation

Install the library using pip:

pip install firejson


---

Features

Validate JSON: Ensure JSON files conform to Firestore's structure and requirements.

Load JSON Files: Read JSON files and prepare them for Firestore population.

Populate Firestore: Insert JSON data into Firestore collections.

Logging: Comprehensive logging for success and error tracking.



---

Example Usage

Below is an example of how to use the library:

1. Prepare Your Service Account Key

Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to point to your Firestore service account key:

export GOOGLE_APPLICATION_CREDENTIALS="path/to/service_account_key.json"

Alternatively, you can set it in your script:

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service_account_key.json"

2. Sample Code

from firejson.core import populate_firestore
from firejson.logging_utils import set_logger

# Initialize a logger (optional)
logger = set_logger()

# Path to the JSON file
file_path = "path/to/example_data.json"

# Firestore collection name
collection_name = "example_collection"

try:
    # Populate Firestore with the JSON data
    populate_firestore(file_path, collection_name, logger)
except ValueError as e:
    print(f"Error: {e}")

3. Example JSON Data

Dictionary Format

{
  "users": [
    {
      "id": "user1",
      "name": "John Doe",
      "email": "johndoe@example.com"
    },
    {
      "id": "user2",
      "name": "Jane Doe",
      "email": "janedoe@example.com"
    }
  ]
}

List Format

[
  {
    "id": "doc1",
    "field1": "value1",
    "field2": "value2"
  },
  {
    "id": "doc2",
    "field1": "value3",
    "field2": "value4"
  }
]

4. Output

If successful, the following logs will be generated:

INFO - Starting Firestore population process...
INFO - JSON structure validated successfully!
INFO - Firestore keys validated successfully!
INFO - Document 'user1' written to collection 'users'.
INFO - Document 'user2' written to collection 'users'.
INFO - Firestore population completed: 2 documents written successfully, 0 failed.

If there's an error, such as an invalid JSON format:

Error: Invalid JSON format in file 'path/to/example_data.json': [error details]


---

License

This project is licensed under the MIT License. See the LICENSE file for details.


---