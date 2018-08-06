#!/usr/bin/env python3

import io
import csv
import xlrd
import utils


def convert_to_csv():
    workbook = xlrd.open_workbook('../data/pmid_22647690/supp_amiajnl-2012-000935_amiajnl-2012-000935supp_table2.xls')
    sheet = workbook.sheet_by_index(0)
    with io.open('../data/pmid_22647690/supp_amiajnl-2012-000935_amiajnl-2012-000935supp_table2.csv', 'w', newline='',
                 encoding='utf-8') as f:
        c = csv.writer(f)
        row_iter = iter(sheet.get_rows())
        # Skip first three rows
        next(row_iter)
        next(row_iter)
        next(row_iter)
        for r in row_iter:
            c.writerow([str(cell.value).strip() for cell in r][0:9])


def map_to_drugbank():
    matched_pairs = []
    matched_triples = []
    existing_pairs = set()
    unmapped_names = set()
    total = 0
    duplicated = 0

    with io.open('../data/pmid_22647690/supp_amiajnl-2012-000935_amiajnl-2012-000935supp_table2.csv', 'r',
                 encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        # 0 - number
        # 1 - drug A
        # 2 - Effect interaction drugA-drugB
        # 3 - drug B
        # 4 - Similar_drug
        # 5 - Tanimoto coefficient (TC)
        # 6 - Name-interaction
        # 7 - Procedence
        # 8 - Interaction explanation
        for row in reader:
            row = [x.strip() for x in row[0:9]]
            total += 1
            id1 = utils.name_to_drugbank_id(row[1])
            id2 = utils.name_to_drugbank_id(row[3])
            id3 = utils.name_to_drugbank_id(row[4])
            if id1 is None:
                unmapped_names.add(row[1])
            if id2 is None:
                unmapped_names.add(row[3])
            if id3 is None:
                unmapped_names.add(row[4])
            direction = row[7].lower()
            #  0 - number
            #  1 - Drugbank A
            #  2 - Drugbank B
            #  3 - Drugbank Similar_drug
            #  4 - drug A
            #  5 - drug B
            #  6 - Similar_drug
            #  7 - Name-interaction
            #  8 - Procedence
            #  9 - Tanimoto coefficient (TC)
            # 10 - Effect interaction drugA-drugB
            # 11 - Interaction explanation
            output = [row[0], id1, id2, id3, row[1], row[3], row[4], row[6], row[7], row[5], row[2], row[8]]
            if id3 is not None:
                id_partner = id1 if direction == 'interaction-a' else (id2 if direction == 'interaction-b' else None)
                if id_partner is not None:
                    if (id3, id_partner) in existing_pairs or (id_partner, id3) in existing_pairs:
                        duplicated += 1
                        continue
                    else:
                        existing_pairs.add((id3, id_partner))
                        matched_pairs.append(output)
                        if id2 is not None and id1 is not None:
                            matched_triples.append(output)

    header = ['number', 'Drugbank A', 'Drugbank B', 'Drugbank Similar_drug', 'drug A', 'drug B', 'Similar_drug',
              'Name-interaction', 'Procedence', 'Tanimoto coefficient (TC)', 'Effect interaction drugA-drugB',
              'Interaction explanation']
    with io.open('../data/pmid_22647690/supp_amiajnl-2012-000935_amiajnl-2012-000935supp_table2_pairs.csv', 'w',
                 newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(header)
        for row in matched_pairs:
            writer.writerow(row)

    with io.open('../data/pmid_22647690/supp_amiajnl-2012-000935_amiajnl-2012-000935supp_table2_triplets.csv', 'w',
                 newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(header)
        for row in matched_triples:
            writer.writerow(row)

    with io.open('../data/pmid_22647690/unmapped_names.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        for row in unmapped_names:
            writer.writerow([row])

    # Matched, Duplicated, Unmatched
    return [len(matched_pairs), duplicated, total - duplicated - len(matched_pairs)]


def process() -> [int]:
    convert_to_csv()
    return map_to_drugbank()


def get_all_interaction_pairs() -> []:
    result = []
    with io.open('../data/pmid_22647690/supp_amiajnl-2012-000935_amiajnl-2012-000935supp_table2_pairs.csv', 'r',
                 encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            procedence = row[8].lower()
            id_partner = row[1] if procedence == 'interaction-a' else (
                row[2] if procedence == 'interaction-b' else None)
            name_partner = row[4] if procedence == 'interaction-a' else (
                row[5] if procedence == 'interaction-b' else None)
            id3 = row[3]
            result.append([id3, row[6], id_partner, name_partner, float(row[9])])
    return result
