# (c) Pranai Rao 2022
# Personal utilities

import pandas as pd

csv_name = "log.csv"  # MUST BE CHANGED FOR OTHER APPLICATIONS!
csv = pd.read_csv(csv_name)

def int_cast_assert(s):
    try:
        s = int(s)
    except ValueError:
        print("\n\n\n\n\n\n\nERROR: Your input is invalid! Please enter an integer!")
    return s


def change_data(row, column, data):
    csv.loc[row, column] = data
    csv.to_csv(csv_name, index=False)


def get_data(row, column):
    return str(csv.loc[row, column])


def add_column(column_name):
    csv[column_name] = ""
    csv.to_csv(csv_name, index=False)


# Confirms the input data before returning input
def affirm(request):
    while True:
        i = input(request)
        affirm = input("You entered \"" + i + "\" Is that correct? (y/n): ")
        if affirm == "y" or affirm == "Y":
            break
    return i
