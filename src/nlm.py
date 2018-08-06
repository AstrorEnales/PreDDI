#!/usr/bin/env python3

import io
import csv
import os.path
import requests

interaction_lookup_url = 'https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=%s&sources=ONCHigh'
drugbank_to_rxcui_map = {}


def save_mapping_table():
    with io.open('../data/nlm/drugbank_rxcui_map.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(['drugbank_id', 'rxcui'])
        for key in sorted(drugbank_to_rxcui_map.keys()):
            writer.writerow([key, drugbank_to_rxcui_map[key]])


def load_mapping_table(drugbank_ids: [str]):
    rxcui_lookup_url = 'https://rxnav.nlm.nih.gov/REST/rxcui.json?idtype=DRUGBANK&id=%s'
    is_dirty = False
    dirty_count = 0
    if os.path.exists('../data/nlm/drugbank_rxcui_map.csv'):
        with io.open('../data/nlm/drugbank_rxcui_map.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                drugbank_to_rxcui_map[row[0]] = row[1]
    for drugbank_id in drugbank_ids:
        if drugbank_id not in drugbank_to_rxcui_map:
            is_dirty = True
            dirty_count += 1
            print('Request RxCUI for DrugBank ID', drugbank_id)
            r = requests.get(rxcui_lookup_url % drugbank_id).json()
            drugbank_to_rxcui_map[drugbank_id] = \
                ';'.join(r['idGroup']['rxnormId']) if 'rxnormId' in r['idGroup'] else None
            if (dirty_count % 50) == 0:
                save_mapping_table()
    if is_dirty:
        save_mapping_table()


def drugbank_to_rxcui(drugbank_id: str) -> str or None:
    return drugbank_to_rxcui_map[drugbank_id] if drugbank_id in drugbank_to_rxcui_map else None
