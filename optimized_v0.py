"""
dynamic programming algorithm that returns the best investment
for more information see the Knapsack problem
"""


import csv
import glob
import pstats
import cProfile
import enquiries
from time import perf_counter


def choose_enquierries(message, options):
    """ask user to choose a file to analyse"""
    print()
    return enquiries.choose(message, options)


def convert_csv_list(csv_name):
    """convert CSV to list.
    exclude stock with value or return < 0 and remove doublons
    """
    file = open(csv_name, "r")
    csv_reader = csv.reader(file)
    next(csv_reader)
    return list({
        (row[0], int(float(row[1])*100), float(row[2])*float(row[1])/100)
        for row in csv_reader
        if float(row[2]) > 0 and float(row[1]) > 0
    })


def get_matrix_best_invest_dynamic_algo(stocks, budget):
    """
    return a 2D matrix
    it calculate the best investment in an incremental way:
    increment the budget from 0 with 1,
    by adding an element to each iteration

    Args:
        stocks ([list]): [each stock contain: name, cost, return]
        budget ([float])

    Returns:
        [2D list]: [matrix]
    """
    matrix = [
        [0 for _ in range(budget + 1)] for _ in range(len(stocks) + 1)
    ]

    for i in range(1, len(stocks) + 1):
        for j in range(1, budget + 1):
            if stocks[i-1][1] > j:
                matrix[i][j] = matrix[i-1][j]
            else:
                matrix[i][j] = max(
                    matrix[i-1][j],
                    stocks[i-1][2] + matrix[i-1][j-stocks[i-1][1]]
                    )
    return matrix


def get_best_invest_from_matrix(stocks, budget, matrix):
    """
    return best investment value and list of stocks
    """
    n = len(stocks)
    best_invest = []
    while budget != 0 and n != 0:
        if matrix[n][budget] != matrix[n - 1][budget]:
            best_invest.append(stocks[n-1])
            budget -= stocks[n-1][1]
        n -= 1
    return matrix[-1][-1], best_invest


def display_results(best_investment):
    """
    print the best investment informations
    """
    stocks_to_buy = [stock[0] for stock in best_investment[1]]
    print(
        f'Stocks to buy : {", ".join(stocks_to_buy)}\n',
        f'Total cost : {sum(stock[1] for stock in best_investment[1])/100}???\n',
        f'Total return : {best_investment[0]}???\n'
    )


def main():

    budget = float(input("Budget client en euros: "))
    budget_cents = int(budget * 100)
    list_files = glob.glob("./csv_to_analyse/*.csv")
    file_name = choose_enquierries("Fichier ?? analyser: ", list_files)

    t1 = perf_counter()
    stocks = convert_csv_list(file_name)
    matrix_knapsack_algo = get_matrix_best_invest_dynamic_algo(
        stocks, budget_cents)
    best_investment = get_best_invest_from_matrix(
        stocks, budget_cents, matrix_knapsack_algo)
    display_results(best_investment)

    t2 = perf_counter()
    print(t2 - t1)


if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='needs_profiling.proof')
