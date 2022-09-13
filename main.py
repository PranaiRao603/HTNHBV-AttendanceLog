# (c) Pranai Rao 2022
# The purpose of this program is to create a log that logs in and out time.
# This program is being built with a barcode interface in mind.

from utilities import *
import pandas as pd
from datetime import datetime

global function_call  # Allows function_call to be accessed from all functions

csv = pd.read_csv("log.csv")  # Opens csv
csv_length = len(csv)

time_index = 0


def menu():
    global function_call
    function_options = """
    1. Create student ID
    2. Sign in/out
    3. Generate Report
    """
    function_range = 3  # Amount of functions specified in the above line.

    print("HTNHBV Entry/Exit Monitor - ON")

    while True:
        print("\n" + function_options)
        function_call = input("Please select a function number: ")
        try:
            function_call = int(function_call)
            if function_call < 1 or function_call > function_range:
                assert 1 > function_call > function_range
        except ValueError:
            print("\n\n\n\n\n\n\nERROR: Your input is invalid! Please enter an integer!")
        except AssertionError:
            print("\n\n\n\n\n\n\nERROR: You have selected a non-existent option!")
        else:
            break

    if function_call == 1:
        create_student_id()
    elif function_call == 2:
        sign_in()
    elif function_call == 3:
        generate_report()


def create_student_id():
    first_name = affirm("Please enter the student's first name: ")
    last_name = affirm("Please enter the student's last name: ")
    change_data(csv_length, 'code', csv_length+1)
    change_data(csv_length, 'first_name', first_name)
    change_data(csv_length, 'last_name', last_name)
    change_data(csv_length, 'status', "OUT")
    print("Added student " + first_name + " " + last_name)
    menu()  # Returns to main menu after completion


def sign_in():
    global time_index
    while True:
        id_num = input("Please enter student ID number (or \'q\' to quit): ")
        if id_num == "q" or id_num == "Q":
            print("HTNHBV Entry/Exit Monitor - RESTARTING...")
            break
        else:
            id_num = int_cast_assert(id_num)
        try:
            this_row = id_num - 1
            if this_row > csv_length - 1:
                raise AssertionError
        except AssertionError:
            print("ERROR: Student ID does not exist")
            continue

        if get_data(this_row, 'status') == 'OUT':
            change_data(this_row, 'status', 'IN')
            change_data(this_row, 'time_in', datetime.now())
        elif get_data(this_row, 'status') == 'IN':
            change_data(this_row, 'status', 'OUT')
            change_data(this_row, 'time_out', datetime.now())

            time_set = "{Sign In: " + get_data(this_row, 'time_in') + " Sign Out: " + get_data(this_row, 'time_out') + \
                       "}"

            open_column = False

            for x in range(0, time_index):
                this_column = 'time' + str(x)
                if get_data(this_row, this_column) == "nan":
                    open_column = this_column
                    break

            if not open_column:
                this_column = 'time' + str(time_index)
                add_column(this_column)
                change_data(this_row, this_column, time_set)
                clear_column('time_in')
                clear_column('time_out')
                time_index += 1

            else:
                change_data(this_row, open_column, time_set)
                clear_column('time_in')
                clear_column('time_out')
    menu()


def generate_report():
    print("WARNING: CONSTRUCTION IN PROGRESS!")


menu()
