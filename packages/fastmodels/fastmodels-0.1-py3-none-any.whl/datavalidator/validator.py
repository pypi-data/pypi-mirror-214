import json
from jsonschema import validate, ValidationError

def validate_json(data):
    """
    Validate a JSON string against the required schema.

    Parameters:
    data (str): The JSON string to validate.

    Returns:
    bool: True if the JSON data matches the schema, False otherwise.
    """

    # Define the expected schema
    schema = {
        "type" : "object",
        "properties" : {
            "prompt" : {"type" : "string"},
            "completion" : {"type" : "string"},
        },
        "required": ["prompt", "completion"],
    }

    try:
        # Parse the JSON data
        json_data = json.loads(data)

        # Validate the JSON data
        validate(instance=json_data, schema=schema)

        # If no exception was raised by validate(), the JSON data is valid
        return True
    except (json.JSONDecodeError, ValidationError):
        # If a JSONDecodeError or ValidationError was raised, the JSON data is invalid
        return False
