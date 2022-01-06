import csv
from time import perf_counter


def convert_csv_list(csv_name):
    file = open(csv_name, "r")
    csv_reader = csv.reader(file)
    next(csv_reader)
    return [
        (row[0], float(row[1]), float(row[2])*float(row[1])/100)
        for row in csv_reader
        if float(row[2]) > 0 and float(row[1]) > 0
    ]


def get_best_investments(list_stocks, budget):

    if not list_stocks:
        return [[], 0, 0], [[]]

    first_element = list_stocks[0]
    best_invest, combination_without_first_elemt = get_best_investments(
        list_stocks[1:], budget
    )

    if first_element[1] > budget:
        return best_invest, combination_without_first_elemt

    combination_with_first_elemt = []

    for comb in combination_without_first_elemt:

        comb_with_first_elemt = [*comb, first_element]
        invest = [
            comb_with_first_elemt,
            sum(stock[1] for stock in comb_with_first_elemt),
            sum(stock[2] for stock in comb_with_first_elemt),
        ]
        if invest[1] <= budget and invest[2] > best_invest[2]:
            best_invest = invest
        combination_with_first_elemt.append(comb_with_first_elemt)

    return best_invest, [
        *combination_without_first_elemt,
        *combination_with_first_elemt,
    ]


# liste = [["a", 10, 60], ["b", 20, 100], ["c", 30, 120]]

file_name = "csv_to_analyse/dataset_test.csv"
stocks = convert_csv_list(file_name)
budget = 500

t1 = perf_counter()

best, combinations = get_best_investments(stocks, budget)
print(f"{best=}")

t2 = perf_counter()

print(t2 - t1)
