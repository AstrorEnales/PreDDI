#!/usr/bin/env python3

import io
import csv
import utils

if __name__ == '__main__':
    all_ddis = {
        'DrugBank': set(),
        'DrugCentral': set()
    }

    with io.open('../data/DrugBank/drug_drug_interactions.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            all_ddis['DrugBank'].add(utils.get_id_pair_tuple(row[0], row[1]))

    with io.open('../data/DrugCentral/drug_interactions.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            all_ddis['DrugCentral'].add(utils.get_id_pair_tuple(row[0], row[1]))

    with io.open('../output/overlap_db_ddis.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        cols = sorted(all_ddis.keys())
        writer.writerow(['id1', 'id2'] + cols)
        all_ddi_pairs = set()
        for key in cols:
            all_ddi_pairs.update(all_ddis[key])
        for row in sorted(all_ddi_pairs):
            writer.writerow([row[0], row[1]] + [1 if row in all_ddis[key] else 0 for key in cols])
