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
    Get data from a CSV file, exclude stock with value or return < 0
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

    matrix = [[0] * (budget + 1)]
    i = 1

    while i < len(stocks) + 1:

        cost_i = stocks[i-1][1]
        matrix_first_part = matrix[i-1][:cost_i].copy()

        matrix_second_part = [
            max(
                matrix[i-1][j],
                stocks[i-1][2] + matrix[i-1][j-stocks[i-1][1]])
            for j in range(cost_i, budget + 1)
        ]

        matrix.append(matrix_first_part.copy()+matrix_second_part.copy())
        i += 1
    return matrix


def get_best_invest_from_matrix(stocks, budget, matrix):

    n = len(stocks)
    best_invest = []
    while budget != 0 and n != 0:
        if matrix[n][budget] != matrix[n - 1][budget]:
            best_invest.append(stocks[n-1])
            budget -= stocks[n-1][1]
        n -= 1
    return matrix[-1][-1], best_invest


def display_results(best_investment):
    stocks_to_buy = [stock[0] for stock in best_investment[1]]
    print(
        f'Stocks to buy : {", ".join(stocks_to_buy)}\n',
        f'Total cost : {sum(stock[1] for stock in best_investment[1])/100}€\n',
        f'Total return : {best_investment[0]}€\n'
    )


def main():

    budget = float(input("Budget client en euros: "))
    budget_cents = int(budget * 100)
    list_files = glob.glob("./csv_to_analyse/*.csv")
    file_name = choose_enquierries("Fichier à analyser: ", list_files)

    t1 = perf_counter()

    stocks = convert_csv_list(file_name)
    matrix_knapsack_algo = get_matrix_best_invest_dynamic_algo(
        stocks, budget_cents)
    best_investment = get_best_invest_from_matrix(stocks, budget_cents,
                                                  matrix_knapsack_algo)
    display_results(best_investment)

    t2 = perf_counter()
    print(t2 - t1)


if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='needs_profiling.proof')
