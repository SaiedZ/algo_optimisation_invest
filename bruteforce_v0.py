"""
brute force algorithm that generates all the combinations
and returns the one that corresponds to the best investment
"""


import csv
import glob
import enquiries
from time import perf_counter


def choose_enquierries(message, options):
    """ask user to choose a file to analyse"""
    print()
    return enquiries.choose(message, options)


def convert_csv_list(csv_name):
    """convert CSV to list.
    Get data from a CSV file, exclude stock with value or return < 0
    """
    file = open(csv_name, "r")
    csv_reader = csv.reader(file)
    next(csv_reader)
    return list({
        (row[0], float(row[1]), float(row[2])*float(row[1])/100)
        for row in csv_reader
        if float(row[2]) > 0 and float(row[1]) > 0
    })


def get_best_investments(list_stocks, budget):
    """
    returns the best investment within a given budget.
    brute force algorithm explore all the combinations
    """
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
        if invest[1] <= budget:
            if invest[2] > best_invest[2]:
                best_invest = invest
            combination_with_first_elemt.append(comb_with_first_elemt)

    return best_invest, [
        *combination_without_first_elemt,
        *combination_with_first_elemt,
    ]


def display_results(best_investment):
    """
    print the best investment informations
    """
    stocks_to_buy = [stock[0] for stock in best_investment[0]]
    print(
        f'Stocks to buy : {", ".join(stocks_to_buy)}\n',
        f'Total cost : {best_investment[1]}€\n',
        f'Total return : {best_investment[2]}€\n'
    )


def main():
    budget = float(input("Budget client en euros: "))
    list_files = glob.glob("./csv_to_analyse/*.csv")
    file_name = choose_enquierries("Fichier à analyser: ", list_files)
    stocks = convert_csv_list(file_name)

    t1 = perf_counter()
    best_investment, combinations = get_best_investments(stocks, budget)
    display_results(best_investment)
    t2 = perf_counter()
    print(t2 - t1)


if __name__ == "__main__":
    main()
