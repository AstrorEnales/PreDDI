#!/usr/bin/env python3

import io
import csv
import os
import tabulate
import nlm
import utils
import drugbank
import process_pmid_22647690
import process_pmid_23520498
import process_pmid_24158091
import process_pmid_26196247
import process_pmid_27354693
import process_pmid_28056782

if __name__ == '__main__':
    modules = {
        22647690: process_pmid_22647690,
        23520498: process_pmid_23520498,
        24158091: process_pmid_24158091,
        26196247: process_pmid_26196247,
        27354693: process_pmid_27354693,
        28056782: process_pmid_28056782
    }

    # Cleanup previous export
    os.remove('../output/master_table.csv')
    os.remove('../output/master_table_top_overlap.csv')
    os.remove('../output/master_table_top_overlap_candidates.csv')

    # Download all supplementary source data
    for key in modules:
        modules[key].download()
    drugbank.prepare()
    utils.load_lookups()
    stats = {key: modules[key].process() for key in modules}
    pmid_link = '[%s](https://www.ncbi.nlm.nih.gov/pubmed/%s)'
    print(tabulate.tabulate([[pmid_link % (key, key)] + stats[key] for key in sorted(stats.keys())],
                            headers=['PMID', 'Matched', 'Duplicated', 'Unmatched'], numalign='right', tablefmt='pipe'))

    mapped_drugbank_ids = set()
    master_table_lookup = {}
    for key in modules:
        for row in modules[key].get_all_interaction_pairs():
            pair_id = utils.get_id_pair_id(row[0], row[2])
            if pair_id not in master_table_lookup:
                mapped_drugbank_ids.add(row[0])
                mapped_drugbank_ids.add(row[2])
                master_table_lookup[pair_id] = {
                    'drugbank_id1': row[0],
                    'kegg_id1': utils.drugbank_to_kegg_id(row[0]),
                    'drug_name1': row[1],
                    'rxcui1': None,
                    'drugbank_id2': row[2],
                    'kegg_id2': utils.drugbank_to_kegg_id(row[2]),
                    'rxcui2': None,
                    'drug_name2': row[3],
                    'drugbank_known': utils.is_drugbank_known_interaction(row[0], row[2]),
                    'kegg_known': utils.is_kegg_known_interaction(row[0], row[2]),
                    'drugs_com_known': utils.is_drugs_com_known_interaction(row[0], row[2]),
                    'unidrug_known': utils.is_unidrug_known_interaction(row[0], row[2]),
                    'sources': {}
                }
            master_table_lookup[pair_id]['sources'][key] = row[-1]

    nlm.load_mapping_table(mapped_drugbank_ids)
    for value in master_table_lookup.values():
        value['rxcui1'] = nlm.drugbank_to_rxcui(value['drugbank_id1'])
        value['rxcui2'] = nlm.drugbank_to_rxcui(value['drugbank_id2'])

    master_table = sorted([x for x in master_table_lookup.values()], key=lambda x: len(x['sources']), reverse=True)
    pmid_keys = sorted(modules.keys())
    header = ['drugbank_id1', 'kegg_id1', 'rxcui1', 'drug_name1',
              'drugbank_id2', 'kegg_id2', 'rxcui2', 'drug_name2',
              'drugbank_known', 'kegg_known', 'drugs_com_known', 'unidrug_known'] + \
             [str(x) for x in pmid_keys]
    # All interactions
    with io.open('../output/master_table.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(header)
        for row in master_table:
            writer.writerow([row[key] for key in header if key in row] +
                            [row['sources'][key] if key in row['sources'] else None for key in pmid_keys])
    # Top overlap list
    with io.open('../output/master_table_top_overlap.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(header)
        for row in master_table:
            if len(row['sources']) < 3:
                continue
            writer.writerow([row[key] for key in header if key in row] +
                            [row['sources'][key] if key in row['sources'] else None for key in pmid_keys])
    # Top overlap list candidates
    with io.open('../output/master_table_top_overlap_candidates.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(header)
        for row in master_table:
            if len(row['sources']) < 3:
                continue
            if row['drugbank_known'] is not None and row['drugbank_known'] != 0:
                continue
            if row['drugs_com_known'] is not None and row['drugs_com_known'] != '0':
                continue
            if row['kegg_known'] is not None and row['kegg_known'] != 0:
                continue
            writer.writerow([row[key] for key in header if key in row] +
                            [row['sources'][key] if key in row['sources'] else None for key in pmid_keys])
