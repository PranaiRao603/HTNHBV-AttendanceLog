# (c) 2022 Pranai Rao
# Helpful utilities


# Safely casts to integer data type
def int_cast_assert(s):
    try:
        s = int(s)
    except ValueError:
        print("\n\n\n\n\n\n\nERROR: Your input is invalid! Please enter an integer!")
    return s


# Confirms the input data before returning input
def affirm(request):
    while True:
        i = input(request)
        confirm = input("You entered \"" + i + "\" Is that correct? (y/n): ")
        if confirm == "y" or confirm == "Y":
            break
    return i
