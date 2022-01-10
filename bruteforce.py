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


def best_invest_brute_force(budget, elements, elements_selection=[]):
    if not elements:
        return sum(i[2] for i in elements_selection), elements_selection

    invest_without_first, list_invest_without_first = best_invest_brute_force(
        budget, elements[1:], elements_selection)
    first_element = elements[0]
    if first_element[1] <= budget:
        invest_with_first, list_invest_with_first = best_invest_brute_force(
            budget - first_element[1],
            elements[1:],
            elements_selection + [first_element]
        )
        if invest_without_first < invest_with_first:
            return invest_with_first, list_invest_with_first

    return invest_without_first, list_invest_without_first


def display_results(best_investment, list_stocks):
    stocks_to_buy = [stock[0] for stock in list_stocks]
    print(
        f'Stocks to buy : {", ".join(stocks_to_buy)}\n',
        f'Total cost : {sum(stock[1] for stock in list_stocks)}€\n',
        f'Total return : {best_investment}€\n'
    )


def main():
    budget = float(input("Budget client en euros: "))
    list_files = glob.glob("./csv_to_analyse/*.csv")
    file_name = choose_enquierries("Fichier à analyser: ", list_files)
    stocks = convert_csv_list(file_name)

    t1 = perf_counter()
    best_investment, list_stocks = best_invest_brute_force(budget, stocks)
    display_results(best_investment, list_stocks)
    t2 = perf_counter()
    print(t2 - t1)


if __name__ == "__main__":
    main()
