import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv', 'new york': 'new_york_city.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    introduction = input("Hey! This is my small program to explore some US bikeshare data! You can choose between: \n - Chicago \n - New York City \n - Washington \nfor a daterange from January to June. It is possible to filter by one of those months or look at \"all\". You can then also filter for a day or just look at the week by selecting \"all\"!\n\nReady? ")
    if introduction.lower() != 'no':
        print("\nCool, lets do it!\n")
    else:
        print("\nToo bad!\n")
        exit()
            
    while True: 
        city = input("Please enter city name ").lower()
        if city in ['chicago', 'washington', 'new york city', 'new york']:
            break
        else: 
            print("Please enter valid city ")

    months_short = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6}
    months_long = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6} #all filter missing
    while True:
        month = input("Which month are you interested in? ").lower()
        if month.lower()=='all':
            break      
        elif month.lower() in months_short:
            month = months_short.get(month.lower())  
            break
        elif month.lower() in months_long:
            month = months_long.get(month.lower())   
            break
        else: 
            print("Please enter valid month ")

    days_short = {'mon':'monday', 'tue':'tuesday', 'wed':'wednesday', 'thu':'thursday', 'fri':'friday', 'sat':'saturday', 'sun':'sunday'}
    days_long = {'monday':'monday', 'tuesday':'tuesday', 'wednesday':'wednesday', 'thursday':'thursday', 'friday':'friday', 'saturday':'saturday', 'sunday':'sunday'}
    while True:
        day = input("For which day? ").lower()
        if day.lower()=='all':
            break        
        elif day.lower() in days_short:
            day = days_short.get(day.lower()) 
            break
        elif day.lower() in days_long:
            day = days_long.get(day.lower()) 
            break
        else:
            print("Please enter a valid day ")

#seems to be redundant since the dictionary means the same as the input. How can I optimize?
#According to mentor: no more efficient way; the use case itself is redundant
#It would be awesome to have the ability choosing between two error messages. The first should display "you can enter the following values" and the second should then loop "Please enter a valid day"
            
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
    
    df = pd.read_csv(CITY_DATA.get(city))
 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    if month!='all':
        df = df[df['Start Time'].dt.month == month]
    
    if day.lower()!='all':
        df = df[df['Start Time'].dt.weekday_name == day.title()]
       
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating the most frequent travel times:\n")
    start_time = time.time()

    most_common_month = df['Start Time'].dt.month.mode()[0]
    months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
    print("The most common month is",months.get(most_common_month))
    
    most_common_day = df['Start Time'].dt.weekday_name.mode()[0]
    print("The most common day is",most_common_day)

    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print("Most people started the ride at",most_common_hour,"O'Clock")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nHere are the most popular stations and trip...\n')
    time.sleep(2)
    start_time = time.time()

    most_common_start = df['Start Station'].mode()[0]
    print("The most common start station is",most_common_start)

    most_common_end = df['End Station'].mode()[0]
    print("The most common end station is",most_common_end)
    
    df['Popular Route']=df['Start Station']+" to "+df['End Station']
    most_common_combi = df['Popular Route'].mode()[0]
    print("The most common route taken is from",most_common_combi)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating trip duration...\n')
    time.sleep(2)
    start_time = time.time()

    sum_trip = df['Trip Duration'].sum()
    print("The total trip time for your selection was",(sum_trip/360),"hours!")   
    
    mean_trip = df['Trip Duration'].mean()
    print("The average trip took around",(mean_trip/60),"minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating user statistics...\n')
    time.sleep(2)
    start_time = time.time()

    count_user = df['User Type'].value_counts()
    print(count_user,"took the bike in your selection")
    
    if 'Gender' in df.columns: 
        count_gender = df['Gender'].value_counts()  
        print(count_gender)
    else:
        print()

    if 'Birth Year' in df.columns:
        birth_min = int(df['Birth Year'].min())
        print("The oldest person was born in",birth_min)
        birth_max = int(df['Birth Year'].max())
        print("The youngest person was born in",birth_max)
        birth_mode = int(df['Birth Year'].mode()[0])
        print("On average the people were born in",birth_mode)    
    else:
        print("There is no data on age or gender for Washington, sorry!")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#I dont want to display the data type -> display_data() ???

def raw_lines(df):
    """
    Prompts the user if they want to see 5 lines of raw data. Displays that
    data if the answer is 'yes'. Continues these prompts and displays until
    the user says 'no'.
    
    source: in collobarotion with student from student hub
    """
    x = 0
    while True:
        if x == 0:
            raw_lines = input("Do yo want to see individual data? (Y/N) ")
            if raw_lines.lower()=='y':
                print(df[x : x +5])
                x = x + 5
            elif raw_lines.lower()=='n':
                break
            else:
                print("Invalid input!")
        else:
            raw_lines = input("\nMore? To exit type 'exit'.\n")
            if raw_lines.lower()=='':
                print(df[x : x +5])
                x = x + 5
            elif raw_lines.lower()=='exit':
                break
            else:
                print("Just click 'enter' or type 'exit'")
#df.iloc() would be an alternative solution

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_lines(df)

        restart = input('\nIf you want to restart type "Yes" otherwise hit any key you want to.\n')
        if restart.lower() != 'yes':
            print('''
                 ______     ________   ______     ________ _ 
                |  _ \ \   / /  ____| |  _ \ \   / /  ____| |
                | |_) \ \_/ /| |__    | |_) \ \_/ /| |__  | |
                |  _ < \   / |  __|   |  _ < \   / |  __| | |
                | |_) | | |  | |____  | |_) | | |  | |____|_|
                |____/  |_|  |______| |____/  |_|  |______(_)
                   _.-._
                 /| | | |_
                 || | | | |
                 || | | | |
                _||     ` |
               \\`\        ;
                \\         |
                 \\       /
                  | |    |
                  | |    |''')
            break

if __name__ == "__main__":
	main()
