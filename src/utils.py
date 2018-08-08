#!/usr/bin/env python3

import io
import csv
import os.path
import urllib.request

pubchem_drugbank_id_map = {}
drugbank_kegg_id_map = {}
drugbank_name_id_map = {}
drugbank_id_name_map = {}
drugbank_product_name_id_map = {}
drugbank_interactions = set()
kegg_interactions = {}
drugs_com_interactions = {}
unidrug_interactions = {}


def load_lookups():
    with io.open('../data/DrugBank/drug links.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            if row[6] is not None and len(row[6]) > 0:
                pubchem_drugbank_id_map[int(row[6])] = row[0]
            if row[5] is not None and len(row[5]) > 0:
                drugbank_kegg_id_map[row[0]] = row[5]

    with io.open('../data/DrugBank/id_name_map.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            drugbank_name_id_map[row[1].lower().strip()] = row[0].strip()

    with io.open('../data/DrugBank/primary_id_name_map.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            drugbank_id_name_map[row[0].strip()] = row[1].lower().strip()

    with io.open('../data/DrugBank/products_id_name_map.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            drugbank_product_name_id_map[row[1].lower().strip()] = row[0].strip()

    with io.open('../data/DrugBank/drug_drug_interactions.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            drugbank_interactions.add(get_id_pair_id(row[0], row[1]))

    with io.open('../data/kegg/drug_pairs.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            kegg_interactions[get_id_pair_id(row[0], row[1])] = int(row[2])

    with io.open('../data/drugs_com/drug_pairs.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            drugs_com_interactions[get_id_pair_id(row[0], row[1])] = row[2]

    with io.open('../data/UniDrug/drug_pairs.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            unidrug_interactions[get_id_pair_id(row[0], row[1])] = int(row[2])


def manual_name_mapping(name: str) -> str or None:
    # Fixed with next DrugBank dump
    # Atracurium
    if name == 'atracurium':
        return 'DB13295'
    # Tenofovir
    if name == 'tenofovir':
        return 'DB14126'

    # Medroxyprogesterone acetate
    if name == 'medroxyprogesterone':
        return 'DB00603'
    # Doxacurium chloride
    if name == 'doxacurium':
        return 'DB01135'
    # Rotigotine
    if name == 'rotigotine/transdermal/patch' or name == 'rotigotine transdermal patch':
        return 'DB05271'

    # Source 2 specific
    # Teriparatide
    if name == 'ly 333334':
        return 'DB06285'
    # Nystatin
    if name == 'nistatin':
        return 'DB00646'
    # Azathioprine
    if name == 'azathioprin':
        return 'DB00993'
    # Desirudin
    if name == 'cgp 39393':
        return 'DB11095'
    # Sodium chloride
    if name == 'nacl':
        return 'DB09153'
    # Budesonide
    if name == 'rhinocort':
        return 'DB01222'
    # Doxycycline
    if name == 'vibramycin':
        return 'DB00254'
    # Cloperastine
    if name == 'hustazol':
        return 'DB09002'

    return None


def name_to_drugbank_id(name: str) -> str or None:
    name_lower = name.lower().replace('/', ' ')
    if name_lower in drugbank_name_id_map:
        return drugbank_name_id_map[name_lower]
    if name_lower in drugbank_product_name_id_map:
        return drugbank_product_name_id_map[name_lower]
    return manual_name_mapping(name_lower)


def drugbank_id_to_name(drugbank_id: str) -> str or None:
    return drugbank_id_name_map[drugbank_id] if drugbank_id in drugbank_id_name_map else None


def pubchem_to_drugbank_id(pubchem_id: str) -> str or None:
    pubchem_id_int = int(pubchem_id[4::])
    return pubchem_drugbank_id_map[pubchem_id_int] if pubchem_id_int in pubchem_drugbank_id_map else None


def drugbank_to_kegg_id(drugbank_id: str) -> str or None:
    return drugbank_kegg_id_map[drugbank_id] if drugbank_id in drugbank_kegg_id_map else None


def is_camel(s):
    return s != s.lower() and s != s.upper()


def get_id_pair_id(id1: str, id2: str) -> str:
    return '%s:%s' % (id1 if id1 < id2 else id2, id2 if id1 < id2 else id1)


def is_drugbank_known_interaction(id1: str, id2: str) -> int or None:
    return 1 if get_id_pair_id(id1, id2) in drugbank_interactions else 0


def is_drugs_com_known_interaction(id1: str, id2: str) -> int or None:
    id_key = get_id_pair_id(id1, id2)
    return drugs_com_interactions[id_key] if id_key in drugs_com_interactions else None


def is_kegg_known_interaction(id1: str, id2: str) -> int or None:
    id_key = get_id_pair_id(id1, id2)
    return kegg_interactions[id_key] if id_key in kegg_interactions else None


def is_unidrug_known_interaction(id1: str, id2: str) -> int or None:
    id_key = get_id_pair_id(id1, id2)
    return unidrug_interactions[id_key] if id_key in unidrug_interactions else None


def download_file(url, filepath):
    if not os.path.exists(filepath):
        print('File does not exist. Trying to download from "%s"...' % url)
        with urllib.request.urlopen(url) as response, open(filepath, 'wb') as f:
            f.write(response.read())
