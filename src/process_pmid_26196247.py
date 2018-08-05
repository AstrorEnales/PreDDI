#!/usr/bin/env python3

import io
import csv
import utils


def map_to_drugbank():
    matched = set()
    results = []
    unmapped = 0
    duplicated = 0

    with io.open('../data/pmid_26196247/DDI_pred.csv', 'r', encoding='utf-8') as f:
        # Drug1_ID, Drug1_Name, Drug2_ID, Drug2_Name, Pred_Score
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            row = [x.strip() for x in row]
            id1 = utils.pubchem_to_drugbank_id(row[0])
            if id1 is None:
                id1 = utils.name_to_drugbank_id(row[1])
            id2 = utils.pubchem_to_drugbank_id(row[2])
            if id2 is None:
                id2 = utils.name_to_drugbank_id(row[3])
            if id1 is None or id2 is None:
                unmapped += 1
                continue
            id_key = '%s:%s' % (id1 if id1 < id2 else id2, id2 if id1 < id2 else id1)
            if id_key not in matched:
                matched.add(id_key)
                results.append([row[0], id1, row[1], row[2], id2, row[3], row[4]])
            else:
                duplicated += 1

    with io.open('../data/pmid_26196247/DDI_pred_mapped.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(['Drug1_ID', 'DrugBank1', 'Drug1_Name', 'Drug2_ID', 'DrugBank2', 'Drug2_Name', 'Pred_Score'])
        for row in results:
            writer.writerow(row)

    # Matched, Duplicated, Unmatched
    return [len(results), duplicated, unmapped]


def process() -> [int]:
    return map_to_drugbank()


def get_all_interaction_pairs() -> []:
    result = []
    with io.open('../data/pmid_26196247/DDI_pred_mapped.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            result.append([row[1], row[2], row[4], row[5], float(row[6])])
    return result
