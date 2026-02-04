import sys
import os
import pandas as pd
import numpy as np


def run_topsis(input_file, weights, impacts, output_file):
    if not os.path.isfile(input_file):
        raise FileNotFoundError("Input file not found")

    try:
        data = pd.read_csv(input_file)
    except Exception:
        raise ValueError("Unable to read input file")

    if data.shape[1] < 3:
        raise ValueError("Input file must contain at least 3 columns")

    criteria = data.iloc[:, 1:]

    criteria = criteria.apply(pd.to_numeric, errors="coerce")
    if criteria.isnull().values.any():
        raise ValueError("Non-numeric value found in criteria columns")

    if len(weights) != criteria.shape[1] or len(impacts) != criteria.shape[1]:
        raise ValueError("Number of weights/impacts must match number of criteria")

    for i in impacts:
        if i not in ['+', '-']:
            raise ValueError("Impacts must be + or -")

    # Step 1: Normalize
    norm = criteria / np.sqrt((criteria ** 2).sum())

    # Step 2: Apply weights
    weighted = norm * weights

    # Step 3: Ideal best and worst
    ideal_best = []
    ideal_worst = []

    for i, impact in enumerate(impacts):
        if impact == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Step 4: Distance calculation
    s_pos = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    s_neg = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    # Step 5: TOPSIS score
    score = s_neg / (s_pos + s_neg)

    # Step 6: Rank
    data['Topsis Score'] = score
    data['Rank'] = data['Topsis Score'].rank(
        ascending=False, method='dense'
    ).astype(int)

    data.to_csv(output_file, index=False)


def main():
    if len(sys.argv) != 5:
        print("Usage: topsis-satyam input.csv \"w1,w2,...\" \"+,-,+,...\" output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    weights = list(map(float, sys.argv[2].split(',')))
    impacts = sys.argv[3].split(',')
    output_file = sys.argv[4]

    try:
        run_topsis(input_file, weights, impacts, output_file)
        print("Output saved to", output_file)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
