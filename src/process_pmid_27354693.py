#!/usr/bin/env python3

import io
import csv
import utils


def map_to_drugbank():
    total = 0
    matched = set()
    results = []
    duplicated = 0

    with io.open('../data/pmid_27354693/DrugBankIDs.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        index = 1
        drugbank_lookup = {}
        for row in reader:
            drugbank_lookup[index] = row[0]
            index += 1

    for i in range(1, 11):
        with io.open('../data/pmid_27354693/%s_interacts_positives.csv' % i, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t', quotechar='"')
            for row in reader:
                total += 1
                id1 = int(row[0].strip())
                id1 = drugbank_lookup[id1] if id1 in drugbank_lookup else None
                id2 = int(row[1].strip())
                id2 = drugbank_lookup[id2] if id2 in drugbank_lookup else None
                # only if both ids were matched
                if id1 is not None and id2 is not None:
                    # duplicate removal
                    id_key = '%s:%s' % (id1 if id1 < id2 else id2, id2 if id1 < id2 else id1)
                    if id_key not in matched:
                        matched.add(id_key)
                        results.append([id1, id2, utils.drugbank_id_to_name(id1), utils.drugbank_id_to_name(id2)])
                    else:
                        duplicated += 1

    with io.open('../data/pmid_27354693/interacts_positives_mapped.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(['id1', 'id2', 'name1', 'name2'])
        for row in results:
            writer.writerow(row)


def process():
    map_to_drugbank()
