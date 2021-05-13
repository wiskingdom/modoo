# built-ins
from functools import reduce
from operator import itemgetter
import json
from openpyxl import Workbook
from os import path, makedirs


def run(input_json_path):

    def each_item_by_name(item_name):
        return lambda acc, curr: [*acc, *curr[item_name]]

    def get_id_form(record):
        _id, form = itemgetter('id', 'form')(record)
        return dict(id=_id, form=f"'{form}")

    with open(input_json_path, 'r', encoding='utf8') as file:
        data = json.load(file)

    docs = data[0]['document'] if isinstance(
        data, list) else data['document']
    snts = reduce(each_item_by_name('sentence'), docs, [])
    id_forms = map(get_id_form, snts)
    filtered = [*filter(lambda x: x['form'], id_forms)]
    print(len(filtered))

    makedirs('./out', exist_ok=True)
    ext_removed = path.splitext(path.normpath(input_json_path))[0]
    file_name = ext_removed.split(path.sep)[-1]
    out_path = f'./out/{file_name}.idform.xlsx'

    wb = Workbook()
    ws = wb.active
    header = ['snt_id', 'snt_form']
    ws.append(header)

    for row in filtered:
        ws.append([*row.values()])

    wb.save(out_path)
