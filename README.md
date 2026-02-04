# TOPSIS-SATYAM-102303729
<br>

```text
This repository contains the implementation of the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) method as part of an academic assignment.
The project is divided into three parts: command-line program, Python package, and a web service.
```

# Part-I: Command Line TOPSIS Program
<br>

```text 
A Python script to compute TOPSIS scores using command-line arguments.
Command format python topsis.py <input_file> <output_file>
Example python topsis.py data.csv "1,1,1,1,1" "+,+,-,+,+" result.csv
Output
Adds Topsis Score and Rank columns to the CSV
Higher score indicates better alternative
```

<br>

# Part-II: Python Package (PyPI)
```text
The TOPSIS program is converted into a Python package and uploaded to PyPI.

PyPI Link
https://pypi.org/project/Topsis-Satyam-102303729/1.0.0/

Installation
pip install Topsis-Satyam-102303729

Usage
topsis-satyam <input_file> "w1,w2,..." "+,-,..." <output_file>

Example
topsis-satyam data.csv "1,1,1,1,1" "+,+,+,+,+" output.csv

If the command is not recognized:
python -m topsis.topsis data.csv "1,1,1,1,1" "+,+,+,+,+" output.csv

A detailed user manual is available in Part2/Readme.md.
```

<br>

# Part-III: TOPSIS Web Service

<br>

```text
A web-based TOPSIS application developed using Flask.
Features
CSV file upload
Weights and impacts input
Email validation
Result CSV sent via email
Workflow
Upload input CSV
Enter weights, impacts, and email ID
TOPSIS is executed on server
Result CSV is emailed to user

```


# Methodology (TOPSIS)

``` text
1-> Normalization: The decision matrix is normalized using vector normalization so that all criteria are dimensionless and comparable.
Formula: rᵢⱼ = xᵢⱼ / √(∑xᵢⱼ²)

2-> Weighting: Each normalized criterion is multiplied by its assigned weight to reflect its importance.
Formula: vᵢⱼ = wⱼ × rᵢⱼ

3-> Ideal Best / Worst: For each criterion, determine the ideal best (maximum for beneficial, minimum for cost) and ideal worst (opposite).

Benefit (+): best = max, worst = min
Cost (−): best = min, worst = max
4->Separation Measures: Calculate the Euclidean distance of each alternative from the ideal best and worst.

Sᵢ⁺ = √(∑(vᵢⱼ − vⱼ⁺)²)
Sᵢ⁻ = √(∑(vᵢⱼ − vⱼ⁻)²)
5-> TOPSIS Score: Compute the relative closeness to the ideal solution.

Cᵢ = Sᵢ⁻ / (Sᵢ⁺ + Sᵢ⁻)
6-> Ranking: Alternatives are ranked based on their TOPSIS scores.
Higher score ⇒ Better rank

```
<br>

# Example Input (data.csv)
| Fund Name | P1  | P2  | P3 | P4  | P5   |
|-----------|-----|-----|----|-----|------|
| M1        | 0.84| 0.71| 6.7| 42.1| 12.59|
| M2        | 0.91| 0.83| 7.0| 31.7| 10.11|
| M3        | 0.79| 0.62| 4.8| 46.7| 13.23|
| M4        | 0.78| 0.61| 6.4| 42.4| 12.55|
| M5        | 0.94| 0.88| 3.6| 62.2| 16.91|
| M6        | 0.88| 0.77| 6.5| 51.5| 14.91|
| M7        | 0.66| 0.44| 5.3| 48.9| 13.83|
| M8        | 0.93| 0.86| 3.4| 37.0| 10.55|

<br>

#  Example Output (result.csv)

| Fund Name |   P1 |   P2 |   P3 |   P4 |   P5 |   Topsis Score |   Rank |
|-----------|-----:|-----:|-----:|-----:|-----:|---------------:|-------:|
| M1        | 0.84 | 0.71 |  6.7 | 42.1 | 12.59 | 0.563692329761227 | 3 |
| M2        | 0.91 | 0.83 |  7.0 | 31.7 | 10.11 | 0.5130321033935658 | 4 |
| M3        | 0.79 | 0.62 |  4.8 | 46.7 | 13.23 | 0.4391772826178256 | 6 |
| M4        | 0.78 | 0.61 |  6.4 | 42.4 | 12.55 | 0.49195608247917144 | 5 |
| M5        | 0.94 | 0.88 |  3.6 | 62.2 | 16.91 | 0.6418858152275323 | 2 |
| M6        | 0.88 | 0.77 |  6.5 | 51.5 | 14.91 | 0.7381481318505098 | 1 |
| M7        | 0.66 | 0.44 |  5.3 | 48.9 | 13.83 | 0.40738953177275933 | 8 |
| M8        | 0.93 | 0.86 |  3.4 | 37.0 | 10.55 | 0.40849867669470064 | 7 |


<br>

# Result Graph:-

<img width="1483" height="759" alt="image" src="https://github.com/user-attachments/assets/3570bfaf-73b7-4b14-b2ba-7c9fc6c0db1f" />


<br>

# Author
<br>

```text
SATYAM
ROLL_NO:102303729
```




