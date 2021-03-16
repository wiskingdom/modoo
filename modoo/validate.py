# built-ins
import json
# third-parties
from jsonschema import validate


def main():
    """
    input_json_name = './data/SXDP2002103120-id-meta.json'
    schema_json_name = './schema/SXDP.scheme.json'
    """
    input_json_name = './data/SXZA2002003110-m-id.json'
    schema_json_name = './schema/XXZA.scheme.json'

    with open(input_json_name, 'r', encoding='utf8') as file:
        data = json.load(file)

    with open(schema_json_name, 'r', encoding='utf8') as file:
        schema = json.load(file)

    validate(instance=data, schema=schema)
