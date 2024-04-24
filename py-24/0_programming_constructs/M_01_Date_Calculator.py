#######################################
# Mission 1: Date Calculator Template #
#######################################

# NOTE: For some test-cases, the standard #print() is used
# For sub-tasks that require more rigorous testing,
# assert f() == ... is used for validating

#############################
# Task 1 - Helper Functions #
#############################

###########
# Task 1a #
###########
def is_leap_year (year: int) -> bool:
    """
    is_leap_year (year) -> boolean
    Function takes in a specific year.
    Returns True if it is a leap year, False otherwise.
    """
    ## Your Code Here ##
    return (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0)
    
# print (is_leap_year(2000)) # True
# print (is_leap_year(1900)) # False
# print (is_leap_year(1984)) # True
# print (is_leap_year(2015)) # False

###########
# Task 1b #
###########
def days_in_month (month: int, is_leap: bool = False) -> int:
    """
    days_in_month (month) -> int
    Function takes in a specific month.
    Returns number of days in that month for a normal year.
    
    Note: This function WILL consider leap year as an OPTIONAL arg defaulted to FALSE
    """
    ## Your Code Here ##
    month_dict = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    return 29 if (month == 2 and is_leap) else month_dict[month - 1]


# ## Print out number of days in each month:
# for i in range (1, 13):
#    print (i, days_in_month(i))
    
# ## Custom cases of February with leap yr in mind
# print("2 in leap", days_in_month(2, is_leap_year(2000)))
# print("2 in not", days_in_month(2, is_leap_year(1900)))


###########
# Task 1c #
###########
def num_of_leap_years (start_year: int, end_year: int):
    """
    num_of_leap_years (start_year, end_year) -> int
    Function takes in 2 years: start_year (inclusive) and end_year (exclusive).
    Returns number of leap years in between the 2 years.
    """
    ## Define num_of_leap_years using iterative loop ##
    ## Your Code Here ##

    # Invalidate if end year earlier
    if end_year < start_year:
        raise ValueError("End year too early")
    
    # Filter out non-leap years in list compre
    leaps_li = [k for k in range(start_year, end_year) if is_leap_year(k)]
    return len(leaps_li)

assert (num_of_leap_years(2010, 2016)) == 1
assert (num_of_leap_years(2008, 2013)) == 2
assert (num_of_leap_years(1900, 2016)) == 28

###########
# Task 1d #
###########

def convert_date(date: str) -> tuple:
    """
    convert_date(date: str) -> (day, month, yr)
    Assume a valid function (try running is_valid_date() first), returns
    ints <day>, <month> and <year> from str numeric <date>
    """
    get_numeric = lambda start, stop: int(date[start:stop])
    return (
        get_numeric(0, 2),
        get_numeric(2, 4),
        get_numeric(4, 9),
    )


def is_valid_date (date: str) -> bool:
    """
    is_valid_date (date) -> boolean
    Function checks if the date entered is a valid date.
    Returns True if it's valid, False otherwise.
    """
    ## Your Code Here ##
    
    # Check input is 8-digit numeric
    if (not date.isdigit()) or len(date) != 8:
        return False
    
    day, month, year = convert_date(date)
    
    # Validate day, month, yr
    if (year < 1900) or (month < 1 or month > 12):
        return False
    return (1 <= day <= days_in_month(month, is_leap_year(year)))

assert is_valid_date("00032015") == False
assert is_valid_date("11092001") == True
assert is_valid_date("11091899") == False
assert is_valid_date("01151900") == False
assert is_valid_date("29022016") == True
assert is_valid_date("31042015") == False
assert is_valid_date("29022015") == False
assert is_valid_date("29022020") == True


###########################
# Task 2 - Main Functions #
###########################

###########
# Task 2a #
###########
def num_of_days_from_1900 (date: str) -> int:
    """
    num_of_days_from_1900 (date) -> int
    Function takes in a date.
    Returns the number of days of the input date after "01011900".
    """
    ## Your Code Here ##
    if not is_valid_date(date):
        raise ValueError("Invalid date given.")
    
    day, month, year = convert_date(date)
    is_leap: bool = is_leap_year(year)

    # Check years (find quant. of leaps & non-leaps)
    y_gap = year - 1900
    y_leaps = num_of_leap_years(1900, year)
    total_days = 366 * y_leaps + 365 * (y_gap - y_leaps)

    # Check months from Jan (for loop thru months)
    for m in range(1, month):
        total_days += days_in_month(m, is_leap)

    # Check days from 01
    total_days += day - 1

    # Return total
    return total_days
    

assert num_of_days_from_1900("30011900") == 29
assert num_of_days_from_1900("03021900") == 33
assert num_of_days_from_1900("28021900") == 58
assert num_of_days_from_1900("11091901") == 618
assert num_of_days_from_1900("01031904") == 1520
assert num_of_days_from_1900("31012016") == 42398


###########
# Task 2b #
###########
def days_between_2_dates (date1: str, date2: str) -> int:
    """
    days_between_2_dates (date1, date2) -> int
    Function takes in 2 dates.
    Returns the number of days in between the 2 dates (no regard for order of dates)
    """
    ## Your Code Here ##
    return abs(num_of_days_from_1900(date2) - num_of_days_from_1900(date1))

# print (days_between_2_dates("15041984", "26102000")) # 6038
# print (days_between_2_dates("26102000", "15041984")) # 6038
# print (days_between_2_dates("26102000", "31012016")) # 5575

###########
# Task 2c #
###########
def add_n_days_after_1900 (days: int) -> str:
    """
    add_n_days_after_1900 (days) -> date
    Function takes in a specific number of days.
    Returns a formatted str numeric date after adding the input number of days to "01011900".
    """
    year, month, day = 1900, 1, 1
    days_left = days

    while days_left > 0:
        days_curr_month = days_in_month(month, is_leap_year(year)) - day + 1

        # Calculate month and see if more months pending
        if days_left >= days_curr_month:
            # Move to the next month
            # And if month > 12, move to next yr
            month += 1
            day = 1
            if month > 12:
                month = 1
                year += 1
            days_left -= days_curr_month
        else:
            day += days_left
            days_left = 0

    # F-formatted with 2 decimal DD, 2 decimal MM, 4 decimal YYYY
    return f"{day:02d}{month:02d}{year:04d}"
    

assert add_n_days_after_1900(30) == "31011900"
assert add_n_days_after_1900(31) == "01021900"
assert add_n_days_after_1900(59) == "01031900"
assert add_n_days_after_1900(420) == "25021901"
assert add_n_days_after_1900(1520) == "01031904"
assert add_n_days_after_1900(88888) == "15052143"
# assert num_of_days_from_1900("15052143") == 88888 

###########
# Task 2d #
###########
def add_n_days_from_a_date (date: str, days: int) -> str:
    """
    add_n_days_from_a_date (date, days) -> date
    Function takes in a date and a specific number of days.
    Returns the date after adding the input number of days to the input date.
    """
    ## Your Code Here ##
    foo = num_of_days_from_1900(date)
    return add_n_days_after_1900(foo + days)


assert add_n_days_from_a_date("15041984", 6038) == "26102000"
assert add_n_days_from_a_date("26102000", 6038) == "08052017"

###########
# Task 2e #
###########
def weekday_of_date (date: str) -> str:
    """
    weekday_of_date (date) -> str
    Function takes in a date.
    Returns the weekday of the input date.
    """
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    idx = num_of_days_from_1900(date) % 7
    return weekdays[idx]

# print(weekday_of_date("01011900")) # "Monday"
# print(weekday_of_date("02011900")) # "Tuesday"
# print(weekday_of_date("31012016")) # "Sunday"

############################
# Task 3 - Date Calculator #
############################
def date_calculator() -> None:
    """
    date_calculator ()
    Function takes in an input from user and performs the functions accordingly.
    """
    try:
        print ("-----------------------------------------")
        print ("Welcome to date calculator")
        print ("  1. Calculate number of days between 2 dates.")
        print ("  2. Add n days from a date.")
        print ("  3. Find weekday of a date.")
        print ("  4. Exit the programme.\n")
        print ("**Please note the format of date should follow the format of 'DDMMYYYY'\n")
        while True:
            
            ## Your Code Here ##
            try:
                option = int(input ("> Select a function: ").strip())
                if not (1 <= option <= 4):
                    raise ValueError
            except ValueError:
                print("[!] Invalid non-int input.")
                continue

            # Tempted to do match-case basis,
            # but held back by potential Python <3.10
            
            if option == 1:
                # Calculate quant. days between 2 dates
                while True:
                    date_1 = input("> Input Date 1: ").strip()
                    if is_valid_date(date_1):
                        break
                while True:
                    date_2 = input("> Input Date 2: ").strip()
                    if is_valid_date(date_2):
                        break
                
                # Comma-formatted in thousands (love f-formats)
                return_sentence = f"[1] > It's {days_between_2_dates(date_1, date_2):,} days between."

            elif option == 2:
                # Add n days from a date
                while True:
                    n = input("> N days: ").strip()
                    if n.isdigit() and int(n) > 0:
                        n = int(n)
                        break
                while True:
                    date = input("> Date: ").strip()
                    if is_valid_date(date):
                        break
                
                return_sentence = f"[2] > {n} days after, it would be {add_n_days_from_a_date(date, n)}."
            
            elif option == 3:
                # Find weekdate
                while True:
                    date = input("> Date: ").strip()
                    if is_valid_date(date):
                        break
                
                return_sentence = f"[3] > That's on a {weekday_of_date(date)}"
            else:
                # Quitting by raising & catching error
                raise KeyboardInterrupt

            print(return_sentence)
    except BaseException:
        print("\nExitted with success code 1. Thank you.")


if __name__ == "__main__":
    date_calculator()
