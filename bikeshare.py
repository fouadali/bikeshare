"""
Author: Fouad Ali Nashat
Email: fouad.nashat@gmail.com
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    month = "all"
    day = "all"
    filter_or_not = "n"
    while True:
        try:
            city = input("Would you like to see data for Chicago, New York, or Washington? [Chicago, New York, Washington]: ").lower()
            if city not in CITY_DATA.keys():
                print("Invalid city selection, please choose one or all of the mentioned cities.")
            else:
                break
        except ValueError:
            print("Invalid city selection, please choose one or all of the mentioned cities.")

    print("You selected: \" {} \"".format(city.title()))
    print('-' * 40 + "\n")

    while True:
        try:
            filter_or_not = input("Would you like to filter the data by month or day? [Y/N]: ").lower()
            if filter_or_not not in ['y', 'n']:
                print("Invalid answer.")
            else:
                break
        except ValueError:
            print("Invalid answer.")

    if filter_or_not == 'y':
        # get user input for month (all, january, february, ... , june)
        while True:
            try:
                month = input("Which month? [All, January, February, March, April, May, or June]: ").lower()

                if month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                    print("Invalid selection.")
                else:
                    break
            except ValueError:
                print("Invalid selection.")

        print("You selected: \" {} \"".format(month.title()))
        print('-' * 20 + "\n")

        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            try:
                day = input(
                    "Which day? [All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday]: ").lower()

                if day not in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
                    print("Invalid selection.")
                else:
                    break
            except ValueError:
                print("Invalid selection.")

        print("You selected: \" {} \"".format(day.title()))
        print('-' * 40 + "\n")

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.dayofweek
    days = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday', 6: 'sunday'}
    df['day_of_week'] = df["day_of_week"].apply(lambda x: days[x])

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[(df['day_of_week'] == day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('-' * 52)
    print('| Calculating The Most Frequent Times of Travel... |')
    print('-' * 52 + '\n')
    start_time = time.time()

    # display the most common month
    temp_month = df['month'].value_counts()
    common_month = temp_month.keys()[0]
    frequency_month = temp_month.values[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    print("The most common month is {}, Count: {}\n".format(months[common_month-1].title(), frequency_month))

    # display the most common day of week
    temp_day = df['day_of_week'].value_counts()
    common_day = temp_day.keys()[0]
    frequency_day = temp_day.values[0]

    print("The most common day of week is {}, Count: {}\n".format(common_day.title(), frequency_day))

    # display the most common start hour
    temp_hour = df['Start Time'].dt.hour.value_counts()
    common_hour = temp_hour.keys()[0]
    frequency_hour = temp_hour.values[0]

    print("The most common start hour is {}, Count: {}\n".format(common_hour, frequency_hour))

    print("This took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n' + '-' * 53)
    print('| Calculating The Most Popular Stations and Trip... |')
    print('-' * 53 + '\n')
    start_time = time.time()

    # display most commonly used start station
    temp_start_station = df['Start Station'].value_counts()
    common_start_station = temp_start_station.keys()[0]
    frequency_start_station = temp_start_station.values[0]
    print("The most commonly used start station is \"{}\", Count: {}\n".format(common_start_station, frequency_start_station))

    # display most commonly used end station
    temp_end_station = df['End Station'].value_counts()
    common_end_station = temp_end_station.keys()[0]
    frequency_end_station = temp_end_station.values[0]
    print("The most commonly used end station is \"{}\", Count: {}\n".format(common_end_station, frequency_end_station))

    # display most frequent combination of start station and end station trip
    temp_start_end_station = (df['Start Station'] + " - " + df['End Station']).value_counts()
    common_start_end_station = temp_start_end_station.keys()[0]
    frequency_start_end_station = temp_start_end_station.values[0]
    print("The most frequent combination of start station and end station trip is \"{}\", Count: {}\n".format(
        common_start_end_station, frequency_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('-' * 32)
    print('| Calculating Trip Duration... |')
    print('-' * 32 + '\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_minutes = int(total_travel_time // 60)
    total_travel_seconds = total_travel_time % 60
    print("The total travel time for all trips is {} Hours {} Minutes {} Seconds (A total of {} seconds.)".format(int(total_travel_minutes // 60), total_travel_minutes % 60, total_travel_seconds, total_travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("The average travel time for all trips is {} Minutes {} Seconds (A total of {} seconds.)".format(int(avg_travel_time // 60), avg_travel_time % 60, avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('-' * 29)
    print('| Calculating User Stats... |')
    print('-' * 29 + '\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:\n", user_types)

    # Display counts of gender
    try:
        gender = df.fillna('Not Specified')['Gender'].value_counts()
        print("\nCounts of Gender:\n", gender)
    except KeyError:
        print("\nGender Information is Not Available for the Selected City.\n")

    # Display earliest, most recent, and most common year of birth
    try:
        most_common_year = df.dropna()['Birth Year'].value_counts().keys()[0]
        sorted_year_of_birth = df.dropna()['Birth Year'].sort_values(ascending=True).values
        print("\nThe earliest year of birth is: {}".format(sorted_year_of_birth[0]))
        print("The most recent year of birth is: {}".format(sorted_year_of_birth[-1]))
        print("The most common year of birth is: {}".format(most_common_year))
    except KeyError:
        print("\nYear of Birth Information is Not Available for the Selected City.\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Display raw data upon request by the user
    """
    cursor = 5
    display = input("Would you like to display trip raw data? [Y/N]: ").lower()
    if display == 'y':
        print(df.iloc[0:cursor])
        while True:
            display = input("Would you like to display 5 more rows? [Y/N]: ").lower()
            if display == 'y':
                print(df.iloc[cursor: cursor+5])
                cursor += 5
            else:
                break
    print('-' * 50)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)
        restart = input('\nWould you like to restart? [Y/N]\n').lower()
        if restart != 'y':
            break


if __name__ == "__main__":
    main()
