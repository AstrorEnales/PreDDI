#!/usr/bin/env python3

import io
import csv
import openpyxl


def convert_to_csv():
    workbook = openpyxl.load_workbook('../data/pmid_28056782/12859_2016_1415_MOESM1_ESM.xlsx')
    sheet = workbook.get_sheet_by_name('ensemble method')
    with io.open('../data/pmid_28056782/12859_2016_1415_MOESM1_ESM.csv', 'w', newline='', encoding='utf-8') as f:
        c = csv.writer(f)
        for r in sheet.rows:
            c.writerow([cell.value for cell in r])


def deduplicate():
    result = []
    existing_pairs = set()
    duplicated = 0

    with io.open('../data/pmid_28056782/12859_2016_1415_MOESM1_ESM.csv', 'r', encoding='utf-8') as f:
        # Drug ID1,Drug ID2,Drug Name1,Drug Name2,Confirm?
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            row = [x.strip() for x in row]
            # Skip unconfirmed
            if row[4] == 'False':
                continue
            if (row[0], row[1]) not in existing_pairs and (row[1], row[0]) not in existing_pairs:
                existing_pairs.add((row[0], row[1]))
                result.append(row[0:-1])
            else:
                duplicated += 1

    with io.open('../data/pmid_28056782/12859_2016_1415_MOESM1_ESM_unique_confirmed.csv', 'w', newline='',
                 encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(['Drug ID1', 'Drug ID2', 'Drug Name1', 'Drug Name2'])
        for row in result:
            writer.writerow(row)


def process():
    convert_to_csv()
    deduplicate()