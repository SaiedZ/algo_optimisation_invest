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
    return [
        (row[0], int(float(row[1])*100), float(row[2])*float(row[1])/100)
        for row in csv_reader
        if float(row[2]) > 0 and float(row[1]) > 0
    ]


def best_invest_dynamic_algo_1time(stocks, budget):

    matrix = [
        [(0, []) for _ in range(budget + 1)] for _ in range(len(stocks) + 1)
    ]
    for i in range(1, len(stocks) + 1):
        for j in range(1, budget + 1):
            if stocks[i-1][1] > j:
                matrix[i][j] = matrix[i-1][j]
            elif (
                matrix[i-1][j][0] < (
                    stocks[i-1][2] + matrix[i-1][j-stocks[i-1][1]][0])):

                matrix[i][j] = (
                    stocks[i-1][2] + matrix[i-1][j-stocks[i-1][1]][0],
                    matrix[i-1][j-stocks[i-1][1]][1] + [stocks[i-1]]
                    )
            else:
                matrix[i][j] = matrix[i-1][j]
    return matrix[-1][-1]


def display_results(best_investment):
    stocks_to_buy = [stock[0] for stock in best_investment[1]]
    print(f'Stocks to buy: {", ".join(stocks_to_buy)}\n')
    print(f"Total cost: {sum(stock[1]/100 for stock in best_investment[1])}\n")
    print(f"Total return: {best_investment[1]}€")


def main():
    t1 = perf_counter()
    budget = float(input("Budget client en euros: "))
    budget_cent = int(budget * 100)
    liste = glob.glob("./csv_to_analyse/*.csv")
    file_name = choose_enquierries("Fichier à analyser: ", liste)
    stocks = convert_csv_list(file_name)
    matrix_knapsack_algo = best_invest_dynamic_algo_1time(stocks,
                                                          budget_cent)
    display_results(matrix_knapsack_algo)

    t2 = perf_counter()
    print(t2 - t1)


if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='needs_profiling.proof')
