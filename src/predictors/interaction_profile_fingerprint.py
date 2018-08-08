#!/usr/bin/env python3

import io
import csv
import numpy as np

if __name__ == '__main__':
    interactions = set()
    labels = set()
    print('Load interactions...')
    with io.open('../../data/DrugBank/drug_drug_interactions.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            labels.add(row[0])
            labels.add(row[1])
            interactions.add((row[0] if row[0] < row[1] else row[1], row[1] if row[0] < row[1] else row[0]))
    labels = sorted(labels)
    label_index_lookup = {labels[i]: i for i in range(0, len(labels))}
    print('%sx%s' % (len(labels), len(labels)))
    print('Build binary interaction matrix M1...')
    m1 = [np.array([0] * len(labels)) for label in labels]
    m2 = [np.array([0.0] * len(labels)) for label in labels]
    m3 = [np.array([0.0] * len(labels)) for label in labels]
    for interaction in interactions:
        i = label_index_lookup[interaction[0]]
        j = label_index_lookup[interaction[1]]
        m1[i][j] = 1
        m1[j][i] = 1

    print('Build Tanimoto-Coefficient matrix M2...')
    counter = 0
    last = 0
    progress_factor = 100.0 / len(labels)
    for i in range(0, len(labels)):
        progress = progress_factor * counter
        if progress % 2 < last:
            print(int(progress), '%')
        counter += 1
        last = progress % 2
        for j in range(0, len(labels)):
            if i != j:
                tanimoto_sum = m1[i] + m1[j]
                x = (tanimoto_sum == 2).sum()
                y = (tanimoto_sum == 1).sum()
                m2[i][j] = x / float(x + y) if x > 0 or y > 0 else 0

    print('Build DDI matrix M3 = M1 x M2...')
    counter = 0
    last = 0
    progress_factor = 100.0 / len(labels)
    for i in range(0, len(labels)):
        progress = progress_factor * counter
        if progress % 2 < last:
            print(int(progress), '%')
        counter += 1
        last = progress % 2
        for j in range(0, len(labels)):
            if i != j:
                m3[i][j] = (m1[i] * m2[j]).max()

    result_interactions = []
    print('Adjust M3 symmetry...')
    for i in range(0, len(labels)):
        for j in range(i + 1, len(labels)):
            maximum = max(m3[i][j], m3[j][i])
            m3[i][j] = maximum
            m3[j][i] = maximum
            if maximum > 0:
                a = labels[i]
                b = labels[j]
                if (a if a < b else b, b if a < b else a) not in interactions:
                    result_interactions.append([a, b, maximum])

    print('Save predicted interactions...')
    result_interactions = sorted(result_interactions, key=lambda x: x[2], reverse=True)
    with io.open('../../output/pred_IPF/predicted_interactions.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(['id1', 'id2', 'tanimoto_coeff'])
        for row in result_interactions:
            writer.writerow(row)
    with io.open('../../output/pred_IPF/predicted_interactions_threshold_70.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(['id1', 'id2', 'tanimoto_coeff'])
        for row in result_interactions:
            if row[2] >= 0.7:
                writer.writerow(row)
    with io.open('../../output/pred_IPF/predictor_ipf_m1.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        for row in m1:
            writer.writerow(row)
    with io.open('../../output/pred_IPF/predictor_ipf_m2.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        for row in m2:
            writer.writerow(row)
    with io.open('../../output/pred_IPF/predictor_ipf_m3.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        for row in m3:
            writer.writerow(row)
