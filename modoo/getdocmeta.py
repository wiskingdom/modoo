# built-ins
from functools import reduce
from os import listdir
import json
# customs
from modoo.idfuncs import jsons_from_dir


def main():

    input_json_name = './data/SXDP2002103120-id.json'
    output_json_name = './out/SXDP2002103120-id-meta.json'
    annotation_level = ['구문 분석']

    """
    input_json_name = './data/SXZA2002003110-m-id.json'
    output_json_name = './out/SXZA2002003110-m-id-meta.json'
    annotation_level = ['무형 대용어 복원']
    """

    rw_dir = './data/1_구어_원시_100만'

    rw_file_names = listdir(rw_dir)
    rw_data = map(jsons_from_dir(rw_dir), rw_file_names)

    def by_meta(acc, curr):
        _id = curr['id']
        meta = curr['metadata']
        acc[_id] = meta
        return acc

    rw_meta_map = reduce(by_meta, rw_data, {})

    def add_meta(doc):
        _id = doc['id']
        metadata = {**rw_meta_map[_id], 'annotation_level': annotation_level}
        return {**doc, 'metadata': metadata}

    def add_to_docs(docs):
        return [*map(add_meta, docs)]

    def add_to_data(data):
        return {**data, 'document': add_to_docs(data['document'])}

    with open(input_json_name, 'r', encoding='utf8') as file:
        data = json.load(file)

    added_data = add_to_data(data)

    with open(output_json_name, 'w', encoding='utf8') as file:
        json.dump(added_data, file, indent=4, ensure_ascii=False)
