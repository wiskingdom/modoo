# built-ins
from functools import reduce
from os import listdir
import json
from collections import defaultdict
import re
# third-parties
from openpyxl import Workbook
# customs
from modoo.idfuncs import jsons_from_dir, get_id_form, by_doc_id, get_id_map


def main():
    dp_file_name = './data/dp1_inputForMapId/SXDP2002103120.json'
    rw_dir = './data/rw_data'

    def each_item_by_name(item_name):
        return lambda acc, curr: [*acc, *curr[item_name]]

    with open(dp_file_name, 'r', encoding='utf8') as file:
        dp_data = json.load(file)

    dp_docs = dp_data['document']
    dp_snts = reduce(each_item_by_name('sentence'), dp_docs, [])
    dp_id_forms = map(get_id_form, dp_snts)

    rw_file_names = listdir(rw_dir)
    rw_data = map(jsons_from_dir(rw_dir), rw_file_names)
    rw_docs = reduce(each_item_by_name('document'), rw_data, [])
    rw_utts = reduce(each_item_by_name('utterance'), rw_docs, [])
    rw_id_forms = map(get_id_form, rw_utts)

    rw_by_doc = reduce(by_doc_id, rw_id_forms, defaultdict(list))
    dp_by_doc = reduce(by_doc_id, dp_id_forms, defaultdict(list))

    def id_mapper(kv):
        k, v = kv
        return get_id_map(rw_by_doc[k], v)

    dp_id_maps = map(id_mapper, dp_by_doc.items())
    dp_id_flats = reduce(
        lambda acc, curr: [*acc, *curr], dp_id_maps, [])

    wb = Workbook()
    ws = wb.active

    header = ['dp_id', 'rw_id', 'dp_form', 'rw_form',
              'id_delay', 'id_step', 'form_exact']
    ws.append(header)

    for row in dp_id_flats:
        ws.append([*row.values()])

    wb.save('./out/dp_id_map.xlsx')