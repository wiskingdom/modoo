# built-ins
from functools import reduce
import json
import re


def main():
    input_json_name = './data/SXDP2002103120+.json'
    id_map_file_name = './data/dp_rw_id_map.txt'

    output_json_name = './out/SXDP2002103120.json'

    def reducer(acc, curr):
        id_pattern = r'(.+)\t(.+)'
        key, value = re.match(id_pattern, curr).groups()
        acc[key] = value
        return acc

    with open(id_map_file_name, 'r', encoding='utf8') as file:
        dp_rw_id_map = reduce(reducer, file.read().strip().split('\n'), {})

    def fix_id(id):
        return dp_rw_id_map[id]

    def fix_snt(snt):
        return {**snt, 'id': fix_id(snt['id'])}

    def fix_snts(snts):
        return [*map(fix_snt, snts)]

    def fix_doc(doc):
        return {**doc, 'sentence': fix_snts(doc['sentence'])}

    def fix_docs(docs):
        return [*map(fix_doc, docs)]

    def fix_data(data):
        return {**data, 'document': fix_docs(data['document'])}

    with open(input_json_name, 'r', encoding='utf8') as file:
        data = json.load(file)

    fixed_data = fix_data(data)

    with open(output_json_name, 'w', encoding='utf8') as file:
        json.dump(fixed_data, file, indent=4, ensure_ascii=False)
