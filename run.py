import calendar
import requests
import pandas

month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
all_countries = requests.get("https://restcountries.com/v2/all").json()


# Get List of countries
def get_countries():
    country_list = []
    for names in all_countries:
        country_list.append(names["name"].title())
    return country_list


# get population of country
def get_population(country_name):
    population_list = []
    for populations in all_countries:
        population_list.append(populations["population"])

    return population_list[get_countries().index(country_name)]


# Get day range of month
def get_day_range(month_name):
    month_range = calendar.monthrange(2020, month_list.index(month_name) + 1)
    return month_range[1]


# Get confirmed cases of country per month
def get_cases_per_month(day, country_name, month_name):
    country_cases = requests.get(f"https://api.covid19api.com/country/{country_name}/"
                                 f"status/confirmed?from=2020-{month_list.index(month_name) + 1}"
                                 f"-{day}T00:00:00Z&to=2020-{month_list.index(month_name) + 1}-{day}T23:59:59Z").json()
    for case in country_cases:
        country_case = case["Cases"]
    return country_case


# Get csv file from api
def get_vaccine_file_from_csv(country_name):
    response = requests.get(f"https://raw.githubusercontent.com/owid/covid-19-data/master/public/data"
                            f"/vaccinations/country_data/{country_name}.csv")
    if response.status_code == 404:
        raise Exception("Seems like rest countries doesn't have same country name!")
    else:
        current_vaccine = pandas.read_csv(f"https://raw.githubusercontent.com/owid/covid-19-data/master/public/data"
                                          f"/vaccinations/country_data/{country_name}.csv")
        return current_vaccine['vaccine'].values[-1]


# Calculate Percentage
def get_cases_in_percentage(cases, population):
    percentage = cases / population * 100
    return round(percentage)


# Validate country input
def test_country_exists(country_name):
    while country_name not in get_countries():
        print("Invalid country. Please try again.")
        country_name = input("Which country you would like for covid cases: ")
        country_name = country_name.title()

    return country_name


# Validate month input
def test_month_exists(month_name):
    while month_name not in month_list:
        print("Invalid month. Please try again.")
        month_name = input("Which month would you like for covid cases(year: 2020): ")
        month_name = month_name.capitalize()

    return month_name


# Get inputs with validation
while True:
    country = input("Which country would you like for covid cases: ")
    country = country.title()
    country = test_country_exists(country)
    month = input("Which month would you like for covid cases(year: 2020): ")
    month = month.capitalize()
    month = test_month_exists(month)
    case_percentage = get_cases_in_percentage(get_cases_per_month(get_day_range(month), country, month),
                                              get_population(country))
    vaccines = get_vaccine_file_from_csv(country.replace(' ', '%20'))
    print(f'Confirmed cases in {month} = {case_percentage}% of the total population of {country}')
    print(f'Currently vaccinating with: {vaccines}')
    while True:
        answer = str(input('Run again? (y/n): '))
        if answer in ('y','n'):
            break
        print("Invalid input.")
    if answer == 'y':
        continue
    else:
        print("Goodbye")
        break
