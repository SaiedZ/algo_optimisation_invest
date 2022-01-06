import csv
from time import perf_counter
import itertools
from math import comb


file_name = "csv_to_analyse/dataset1_Python+P7.csv"


def convert_csv_list(csv_name):
    file = open(csv_name, "r")
    csv_reader = csv.reader(file)
    next(csv_reader)
    return {
        row[0]: [float(row[1]), float(row[2])]
        for row in csv_reader
        if float(row[2]) != 0 and float(row[1]) != 0
    }


def get_best_investment(budget, stocks, combinations):
    best_investment = [[""], 0, 0]
    for combination in combinations:
        investment = [
            combination,
            sum(stocks[stock][0] for stock in combination),
            sum(stocks[stock][0] * stocks[stock][1] / 100 for stock in combination),
        ]
        if investment[1] <= budget and investment[2] > best_investment[2]:
            best_investment = investment

    return best_investment


def get_best_portfolio(budget, stocks):
    best_investment = [[""], 0, 0]
    for i in range(1, len(stocks) + 1):
        combinations = itertools.combinations(stocks, i)
        selectionned_investment = get_best_investment(budget, stocks, combinations)
        if best_investment[2] < selectionned_investment[2]:
            best_investment = selectionned_investment
        print(
            f"nombre d'élements par combinaison: {i}, le meilleur invest est {best_investment}"
        )
    return best_investment


t1 = perf_counter()
budget = 500
stocks = convert_csv_list(file_name)
best_investment = get_best_portfolio(budget, stocks)
print(best_investment)
t2 = perf_counter()

print(t2 - t1)
