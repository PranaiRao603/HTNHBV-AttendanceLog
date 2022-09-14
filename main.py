# (c) Pranai Rao 2022
# The purpose of this program is to create a log that logs in and out time.
# This program is being built with a barcode interface in mind.
# v.3.0.0

import pandas as pd
from utilities import *
from datetime import datetime
import os

log = pd.read_csv("time_log.csv")  # Opens CSV for storing complete data sets
status = pd.read_csv("status.csv")  # Opens CSV for storing temporary data


def get_log_length():
    return len(log)


def get_status_length():
    return len(status)


def menu():
    function_options = """
    1. Create student ID
    2. Sign in/out
    3. Generate report
    4. Delete all temporary data (to be done after report is generated)
    5. Shut down
    """
    function_range = 5  # Amount of functions specified in the above line

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
        logger()
    elif function_call == 3:
        generate_report()
    elif function_call == 4:
        delete_temp_data()
    elif function_call == 5:
        shut_down()


def change_data(file_variable, file_name, row, column, data):
    file_variable.loc[row, column] = data
    file_variable.to_csv(file_name, index=False)


def add_column(file_variable, file_name, column_name):
    file_variable[column_name] = ""
    file_variable.to_csv(file_name, index=False)


def create_student_id():
    status_length = get_status_length()
    first_name = affirm("Please enter the student's first name: ")
    last_name = affirm("Please enter the student's last name: ")
    name = first_name + "_" + last_name

    change_data(status, 'status.csv', status_length, 'code', status_length + 1)
    change_data(status, 'status.csv', status_length, 'name', name)
    change_data(status, 'status.csv', status_length, 'status', 'OUT')

    add_column(log, 'time_log.csv', name)

    print("Added student " + first_name + " " + last_name)
    menu()


def get_data(file_variable, row, column):
    return str(file_variable.loc[row, column])


def logger():
    while True:
        status_length = get_status_length()
        log_length = get_log_length()

        id_num = input("Please enter student ID number (or \'q\' to quit): ")
        if id_num == "q" or id_num == "Q":
            print("HTNHBV Entry/Exit Monitor - RESTARTING...")
            menu()
            break
        else:
            id_num = int_cast_assert(id_num)
        try:
            this_row = id_num - 1
            if this_row > status_length - 1:
                raise AssertionError
        except AssertionError:
            print("ERROR: Student ID does not exist")
            continue

        if get_data(status, this_row, 'status') == "OUT":
            change_data(status, 'status.csv', this_row, 'status', 'IN')
            change_data(status, 'status.csv', this_row, 'time_in', datetime.now())

            name = get_data(status, this_row, 'name')
            time_in = get_data(status, this_row, 'time_in')

            print(name + " was signed in at " + time_in)

        elif get_data(status, this_row, 'status') == "IN":
            change_data(status, 'status.csv', this_row, 'status', 'OUT')
            change_data(status, 'status.csv', this_row, 'time_out', datetime.now())

            name = get_data(status, this_row, 'name')
            time_in = get_data(status, this_row, 'time_in')
            time_out = get_data(status, this_row, 'time_out')

            time_set = "{Sign In: " + time_in + " Sign Out: " + time_out + "}"
            change_data(log, 'time_log.csv', log_length, name, time_set)

            change_data(status, 'status.csv', this_row, 'time_in', '')
            change_data(status, 'status.csv', this_row, 'time_out', '')

            print(name + " was signed out at " + time_out)


def get_row_from_name(name):
    status_length = len(status)
    for x in range(0, status_length):
        if get_data(status, x, 'name') == name:
            return x
        # Else, the student does not exist and a fatal error will occur


def generate_report():
    status_length = get_status_length()
    log_length = get_log_length()

    date = str(datetime.now().date())
    file_name = "Attendance-Log_" + date + ".txt"

    present_list = []
    error_list = []
    absent_list = []

    try:
        open(file_name, 'xt')
    except FileExistsError:
        while True:
            i = input("A report already exists for today. Would you like to replace it? (y/n): ")
            if i == "y" or i == "Y":
                os.remove(file_name)
                open(file_name, 'xt')
                break
            else:
                print("HTNHBV Entry/Exit Monitor - Shutting down...")
                return
    for x in range(0, status_length):
        name = get_data(status, x, 'name')
        time_set = ''
        for y in range(0, log_length):
            if get_data(log, y, name) == 'nan':
                continue
            time_set += " " + get_data(log, y, name)
        if time_set != '':
            present_list.append("PRESENT: " + name + " -" + time_set + "\n")
        else:
            if get_data(status, get_row_from_name(name), 'status') == "IN":
                error_list.append("IN: " + name + " Signed in at: " +
                                  get_data(status, get_row_from_name(name), 'time_in') + "\n")
            else:
                absent_list.append("ABSENT: " + name + "\n")

    present_list = sorted(present_list)
    error_list = sorted(error_list)
    absent_list = sorted(absent_list)

    f = open(file_name, 'a')

    f.write("Present: \n\n")
    for x in range(0, len(present_list)):
        f.write(present_list[x])

    f.write("\nSigned In: \n\n")
    for x in range(0, len(error_list)):
        f.write(error_list[x])

    f.write("\nAbsent: \n\n")
    for x in range(0, len(absent_list)):
        f.write(absent_list[x])

    f = open(file_name, 'r')
    f.close()

    print("Report generated!")
    menu()


def delete_temp_data():
    status_length = get_status_length()
    global log

    affirm("""WARNING: Would you like to delete the data? (y/n): """)

    # Clearing log
    os.remove('time_log.csv')
    open('time_log.csv', 'xt')
    name_list = ""
    for x in range(0, status_length):
        data = get_data(status, x, 'name')
        if data != "nan":
            if x != status_length - 1:
                name_list += get_data(status, x, 'name') + ","
            else:
                name_list += get_data(status, x, 'name')
    f = open('time_log.csv', 'a')
    f.write(name_list)
    f.close()

    # Clearing status
    for x in range(0, status_length):
        change_data(status, 'status.csv', x, 'status', 'OUT')
        change_data(status, 'status.csv', x, 'time_in', '')
        change_data(status, 'status.csv', x, 'time_out', '')

    print("Temporary data cleared!")
    menu()


def shut_down():
    print("Shutting down...")
    print("HTNHBV Entry/Exit Monitor - OFF")


menu()
