# built-ins
from functools import reduce
from os import listdir, path, makedirs
import json
from collections import defaultdict
# third-parties
from openpyxl import Workbook
# customs
from modoo.idfuncs import jsons_from_dir, get_id_form, by_doc_id, get_id_map


def run(input_json_path, rw_dir_path):
    def each_item_by_name(item_name):
        return lambda acc, curr: [*acc, *curr[item_name]]

    print(f'read: {input_json_path}')

    with open(input_json_path, 'r', encoding='utf8') as file:
        dp_data = json.load(file)

    dp_docs = dp_data['document']
    dp_snts = reduce(each_item_by_name('sentence'), dp_docs, [])
    dp_id_forms = map(get_id_form, dp_snts)

    print(f'read: {rw_dir_path}')

    rw_file_names = listdir(rw_dir_path)
    rw_data = map(jsons_from_dir(rw_dir_path), rw_file_names)
    rw_docs = reduce(each_item_by_name('document'), rw_data, [])
    rw_utts = reduce(each_item_by_name('utterance'), rw_docs, [])
    rw_id_forms = map(get_id_form, rw_utts)

    rw_by_doc = reduce(by_doc_id, rw_id_forms, defaultdict(list))
    dp_by_doc = reduce(by_doc_id, dp_id_forms, defaultdict(list))

    print('process: get id map')

    def id_mapper(kv):
        k, v = kv
        return get_id_map(rw_by_doc[k], v)

    dp_id_maps = map(id_mapper, dp_by_doc.items())
    dp_id_flats = reduce(
        lambda acc, curr: [*acc, *curr], dp_id_maps, [])

    wb = Workbook()
    ws = wb.active

    header = ['an_id', 'rw_id', 'an_form', 'rw_form',
              'id_delay', 'id_step', 'exact_form', 'exact_id']
    ws.append(header)

    for row in dp_id_flats:
        ws.append([*row.values()])

    makedirs('./out', exist_ok=True)
    ext_removed = path.splitext(path.normpath(input_json_path))[0]
    file_name = ext_removed.split(path.sep)[-1]

    out_path = f'./out/{file_name}.idmap.xlsx'
    print(f'write: {out_path}')

    wb.save(out_path)
    print('DONE!!')
