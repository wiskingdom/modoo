# built-ins
import json
import sys
# third-parties
from jsonschema import Draft7Validator


def main():
    """
    input_json_name = './data/SXDP2002103120-id-meta.json'
    schema_json_name = './schema/XXDP.scheme.json'
    """
    input_json_name = './data/za4_result/SXZA2002003110-mg-id-meta.json'
    schema_json_name = './schema/XXZA.scheme.json'
    log_name = './out/SXZA2002003110-mg-id-meta.log.txt'

    with open(input_json_name, 'r', encoding='utf8') as file:
        data = json.load(file)

    with open(schema_json_name, 'r', encoding='utf8') as file:
        schema = json.load(file)

    v = Draft7Validator(schema)

    errors = sorted(v.iter_errors(data), key=lambda e: e.path)

    with open(log_name, 'w', encoding='utf8') as file:
        sys.stdout = file
        for error in errors:
            print(error)
            print('-----------------------')
