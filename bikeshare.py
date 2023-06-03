import time
import pandas as pd
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    while True:
        city = input("Would you like to see data for Chicago, New York, or Washington? ").lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print("Invalid input! Please enter a valid city.")

     # get user input for filtering option (month, day, both, none)
    while True:
        filter_option = input("Would you like to filter the data by month, day, both, or none? ").lower()
        if filter_option in ['month', 'day', 'both', 'none']:
            break
        else:
            print("Invalid input! Please enter a valid option.")

    # get user input for month (if selected)
    if filter_option in ['month', 'both']:
        while True:
            month = input("Enter the month to analyze (January, February, ...): ").title()
            if month in ['January', 'February', 'March', 'April', 'May', 'June']:
                break
            else:
                print("Invalid input! Please enter a valid month.")
    else:
        month = 'all'

    # get user input for day of week (if selected)
    if filter_option in ['day', 'both']:
        while True:
            day = input("Enter the day of the week to analyze (Monday, Tuesday, ...): ").title()
            if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                break
            else:
                print("Invalid input! Please enter a valid day of the week.")
    else:
        day = 'all'

    print('-'*40)
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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the "Start Time" column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week from "Start Time"
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Filter the dataframe based on user input
    if month != 'all':
        month_num = pd.to_datetime(month, format='%B').month
        df = df[df['Month'] == month_num]

    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month_num = df['Month'].mode()[0]
    common_month_name = calendar.month_name[common_month_num]
    print("The most common month: ", common_month_name)

    # display the most common day of week
    common_day = df['Day of Week'].mode()[0]
    print("The most common day of the week: ", common_day)

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print("The most common start hour: ", common_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station: ", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station: ", common_end_station)

    # display most frequent combination of start station and end station trip
    frequent_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination of start station and end station trip: ")
    print(f"Start Station: {frequent_combination[0]}, End Station: {frequent_combination[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: ", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: ", mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_counts)
    else:
        print("\nGender information is not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]

        print("\nEarliest birth year: ", int(earliest_birth_year))
        print("Most recent birth year: ", int(most_recent_birth_year))
        print("Most common birth year: ", int(most_common_birth_year))
    else:
        print("\nBirth year information is not available for this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_filter_info(city, month, day, entry_count):
    """Prints the filter information and count of entries."""

    print("\nFilter Information:")
    print("City: ", city.title())
    print("Month: ", month.title())
    print("Day: ", day.title())
    print("Number of Entries: ", entry_count)
    print('-' * 40)
    
def display_data(df):
    """Displays rows of data based on user input."""

    start_row = 0
    display_rows = 5

    while True:
        # Display rows of data
        print(df.iloc[start_row : start_row + display_rows])

        # Ask user if they want to see more rows
        show_more = input('\nDo you want to see the next {} rows of data? Enter yes or no.\n'.format(display_rows))
        
        # Update the start_row value to display the next set of rows
        start_row += display_rows
        
        if show_more.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)
        print_filter_info(city, month, day, len(df))
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Ask user if they want to see rows of data
        while True:
            show_data = input('\nWould you like to see 5 rows of individual trip data? Enter yes or no.\n')
            if show_data.lower() == 'yes':
                display_data(df)
                break
            elif show_data.lower() == 'no':
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes':
                break
            elif restart.lower() == 'no':
                return
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")


if __name__ == "__main__":
	main()
