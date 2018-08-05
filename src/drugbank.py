#!/usr/bin/env python3

import io
import csv
import os.path
import xml.etree.ElementTree as etree


def prepare():
    if os.path.exists('../data/DrugBank/primary_id_name_map.csv') and os.path.exists(
            '../data/DrugBank/id_name_map.csv') and os.path.exists('../data/DrugBank/products_id_name_map.csv'):
        return

    drugs_id_map = {}
    products_id_map = {}
    primary_id_name_map = {}

    ns = '{http://www.drugbank.ca}'

    with io.open('../data/DrugBank/full database.xml', 'r', encoding='utf-8') as f:
        tree = etree.parse(f)
        root = tree.getroot()

        for elem in root.findall(ns + 'drug'):
            ids = elem.findall(ns + 'drugbank-id')
            if len(ids) == 0:
                continue
            primary_ids = [x for x in ids if 'primary' in x.attrib and x.attrib['primary'] == 'true']
            drugbank_id = primary_ids[0].text if len(primary_ids) > 0 else ids[0].text
            if drugbank_id is None:
                continue

            name_node = elem.find(ns + 'name')
            if name_node is not None and name_node.text is not None:
                if drugbank_id not in drugs_id_map:
                    drugs_id_map[drugbank_id] = set()
                drugs_id_map[drugbank_id].add(name_node.text)
                primary_id_name_map[drugbank_id] = name_node.text
                synonyms_node = elem.find(ns + 'synonyms')
                if synonyms_node is not None:
                    for synonym in synonyms_node.findall(ns + 'synonym'):
                        if synonym is not None and synonym.text is not None:
                            drugs_id_map[drugbank_id].add(synonym.text)

                products = elem.find(ns + 'products')
                if products is not None:
                    for product in products.findall(ns + 'product'):
                        name_node = product.find(ns + 'name')
                        if name_node is not None and name_node.text is not None:
                            if drugbank_id not in products_id_map:
                                products_id_map[drugbank_id] = set()
                            products_id_map[drugbank_id].add(name_node.text)

    with io.open('../data/DrugBank/primary_id_name_map.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(['id', 'name'])
        for drug_id in sorted(primary_id_name_map.keys()):
            writer.writerow([drug_id, primary_id_name_map[drug_id]])

    with io.open('../data/DrugBank/id_name_map.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(['id', 'name'])
        for drug_id in sorted(drugs_id_map.keys()):
            for name_node in sorted(drugs_id_map[drug_id]):
                writer.writerow([drug_id, name_node])

    with io.open('../data/DrugBank/products_id_name_map.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(['id', 'name'])
        for product_id in sorted(products_id_map.keys()):
            for name_node in sorted(products_id_map[product_id]):
                writer.writerow([product_id, name_node])
