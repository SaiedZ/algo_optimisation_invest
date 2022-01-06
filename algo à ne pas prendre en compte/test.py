import glob
import enquiries


def choose_enquierries(message, options):
    print()
    return enquiries.choose(message, options)


liste = glob.glob("./csv_to_analyse/*.csv")
choix = choose_enquierries("choisir", liste)
print(choix)
