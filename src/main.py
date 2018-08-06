#!/usr/bin/env python3

import io
import csv
import shutil
import os.path
import tabulate
import urllib.request
import nlm
import utils
import drugbank
import process_pmid_22647690
import process_pmid_23520498
import process_pmid_24158091
import process_pmid_26196247
import process_pmid_27354693
import process_pmid_28056782


def download_file(url, filepath):
    if not os.path.exists(filepath):
        print('File does not exist. Trying to download...')
        with urllib.request.urlopen(url) as response, open(filepath, 'wb') as f:
            f.write(response.read())


def download_sources():
    # Download supplementary data from PMID 28056782
    download_file('https://static-content.springer.com/esm/art%3A10.1186%2Fs12859-016-1415-9/MediaObjects/' +
                  '12859_2016_1415_MOESM1_ESM.xlsx', '../data/pmid_28056782/12859_2016_1415_MOESM1_ESM.xlsx')
    # Download supplementary data from PMID 26196247
    download_file('http://astro.temple.edu/~tua87106/DDI_pred.csv', '../data/pmid_26196247/DDI_pred.csv')
    # Download supplementary data from PMID 23520498
    download_file('https://doi.org/10.1371/journal.pone.0058321.s001',
                  '../data/pmid_23520498/journal.pone.0058321.s001.XLSX')
    # Download supplementary data from PMID 27354693
    download_file('https://bitbucket.org/linqs/psl-drug-interaction-prediction/raw/' +
                  '35fbfd84e56e3cdb3248d376359dfa2b13ecb630/DrugBankIDs', '../data/pmid_27354693/DrugBankIDs.csv')
    for i in range(1, 11):
        download_file('https://bitbucket.org/linqs/psl-drug-interaction-prediction/raw/' +
                      '35fbfd84e56e3cdb3248d376359dfa2b13ecb630/data/all_dataset2/all/%s/interacts_positives.csv' % i,
                      '../data/pmid_27354693/%s_interacts_positives.csv' % i)
    # Download supplementary data from PMID 24158091
    download_file('https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3932451/bin/amiajnl-2013-001612-s3.csv',
                  '../data/pmid_24158091/amiajnl-2013-001612-s3.csv')
    # Download supplementary data from PMID 22647690
    download_file('https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3534468/bin/' +
                  'supp_amiajnl-2012-000935_amiajnl-2012-000935supp_table2.xls',
                  '../data/pmid_22647690/supp_amiajnl-2012-000935_amiajnl-2012-000935supp_table2.xls')


if __name__ == '__main__':
    # Cleanup previous export
    if os.path.exists('../output/') and os.path.isdir('../output/'):
        shutil.rmtree('../output/')
    os.mkdir('../output/')

    download_sources()
    drugbank.prepare()
    utils.load_lookups()
    modules = {
        22647690: process_pmid_22647690,
        23520498: process_pmid_23520498,
        24158091: process_pmid_24158091,
        26196247: process_pmid_26196247,
        27354693: process_pmid_27354693,
        28056782: process_pmid_28056782
    }
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
                    'drugbank_known': 1 if utils.is_known_interaction(row[0], row[2]) else 0,
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
              'drugbank_known'] + \
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
