#!/usr/bin/env python3

import io
import csv
import openpyxl
import utils


def convert_to_csv():
    workbook = openpyxl.load_workbook('../data/pmid_23520498/journal.pone.0058321.s001.xlsx')
    sheet = workbook.get_active_sheet()
    with io.open('../data/pmid_23520498/journal.pone.0058321.s001.csv', 'w', newline='', encoding='utf-8') as f:
        c = csv.writer(f)
        row_iter = iter(sheet.rows)
        # Skip first three rows
        next(row_iter)
        next(row_iter)
        next(row_iter)
        for r in row_iter:
            c.writerow([cell.value for cell in r][0:6])


def map_to_drugbank():
    matched_pairs = []
    matched_triples = []
    existing_pairs = set()
    total = 0
    duplicated = 0

    with io.open('../data/pmid_23520498/journal.pone.0058321.s001.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        # 0 - Number
        # 1 - DrugA
        # 2 - DrugC: similar to DrugA
        # 3 - DrugB
        # 4 - TC
        # 5 - Effect drugC-drugB (the effect drugA-drugB is similar to drugC-drugB according to the model.
        #     To interpret the interaction drugC should be substituted by drugA)
        for row in reader:
            row = [x.strip() for x in row]
            total += 1
            id1 = utils.name_to_drugbank_id(row[1])
            id2 = utils.name_to_drugbank_id(row[2])
            id3 = utils.name_to_drugbank_id(row[3])
            if id1 is not None and id3 is not None:
                # 0 - Number
                # 1 - DrugbankA
                # 2 - DrugbankC
                # 3 - DrugbankB
                # 4 - DrugA
                # 5 - DrugC: similar to DrugA
                # 6 - DrugB
                # 7 - TC
                # 8 - Effect drugC-drugB
                output = [row[0], id1, id2, id3, row[1], row[2], row[3], row[4], row[5]]
                if (id1, id3) in existing_pairs or (id3, id1) in existing_pairs:
                    duplicated += 1
                    continue
                existing_pairs.add((id1, id3))
                matched_pairs.append(output)
                if id2 is not None:
                    matched_triples.append(output)

    with io.open('../data/pmid_23520498/journal.pone.0058321.s001_pairs.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        for row in matched_pairs:
            writer.writerow(row)

    with io.open('../data/pmid_23520498/journal.pone.0058321.s001_triplets.csv', 'w', newline='',
                 encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        for row in matched_triples:
            writer.writerow(row)


def process():
    convert_to_csv()
    map_to_drugbank()
