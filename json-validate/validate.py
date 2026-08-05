import json
from jsonschema import validate, ValidationError
import logging

def validate_json(data_path, schema_path):
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    with open(schema_path, "r") as f:
        schema = json.load(f)

    with open(data_path,"r") as f:
        data = json.load(f)

    try: 

        validate(instance=data, schema=schema)
        log.info(f" {data_path} file is OK")
    except ValidationError as e:
        print(f"Fail: {e.message}")


validate_json("data.json","schema.json")