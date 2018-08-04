#!/usr/bin/env python3

import os.path
import urllib.request
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
    download_sources()
    process_pmid_28056782.process()
