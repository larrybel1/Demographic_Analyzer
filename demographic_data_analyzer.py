import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult_data.csv')
    # print(df.head())

    # # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts().reset_index()
    race_count.columns = ['race' , 'count']
    race_count = race_count['count'].to_list()#.to_string()
    # print(race_count)
    

    # What is the average age of men? 
    sex_age = df[['sex' , 'age']]
    men_age = sex_age.loc[sex_age['sex'] == 'Male']
    average_age_men = men_age['age'].mean().round(1)
    # print(average_age_men)
    # print(men_age)

    # What is the percentage of people who have a Bachelor's degree?
    education = df[['education']].value_counts()
    percentage_bachelors = ((education['Bachelors'] / len(df[['education']])) * 100).round(1) #/ education[''].sum() )* 100 
    # print(percentage_bachelors)


    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    ed_salary = df[['education', 'salary']] #print(type(ed_salary))
    ed_level= ed_salary.sort_values( by = 'education')

    education_rich = ed_salary[ed_salary['education'].isin(['Bachelors' , 'Masters' , 'Doctorate'])]#.value_counts()#, ed_salary['salary'].isin['>50K']))
    ed_rich_sum = education_rich.value_counts().sum()
    education_rich_num = education_rich[education_rich['salary'].isin(['>50K'])].value_counts().sum()

    # None higher education people 
    noned_rich = ed_salary[~ed_salary['education'].isin(['Bachelors' , 'Masters' , 'Doctorate'])]#.value_counts()#, ed_salary['salary'].isin['>50K']))
    noned_rich_sum = noned_rich.value_counts().sum()
    noned_rich_num = noned_rich[noned_rich['salary'].isin(['>50K'])].value_counts().sum()


    higher_education_rich = ((education_rich_num / ed_rich_sum) * 100).round(1)
    lower_education_rich = ((noned_rich_num / noned_rich_sum) * 100).round(1)
    # print(higher_education_rich)
    # print(lower_education_rich)

    # advance_ed = ed_level[ed_level['education'].isin(['Bachelors' , 'Masters' , 'Doctorate'])]#, axis = 1, level = 1) # [ 'Bachelors' , 'Masters' , 'Doctorate']
    # none_advance_ed = ed_level[~ed_level['education'].isin(['Bachelors' , 'Masters' , 'Doctorate'])]
  

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = (df['hours-per-week'].min()).round(1)
    # print(min_work_hours)

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    hours_salary = df[['hours-per-week', 'salary']]

    num_min_workers = len(hours_salary.loc[(hours_salary['hours-per-week'] == 1) & (hours_salary['salary'] == '>50K')])
    rich_percentage = (num_min_workers / len(hours_salary.loc[hours_salary['hours-per-week'] == 1])) * 100#.round(1)
    # print(rich_percentage)

    # What country has the highest percentage of people that earn >50K?
    rate_rich = pd.DataFrame(columns = ['native-country', 'rich-rate'])
    earnings = df[['salary', 'native-country']]
    earnings = earnings.sort_values(by = 'salary')
    rich_country = earnings.loc[(earnings['salary'] == '>50K')]
    rich_country_count = rich_country ['native-country'].value_counts().reset_index()
    rich_country_count.columns = ['native country', 'count']
    country_count = earnings['native-country'].value_counts().reset_index()
    country_count.columns = ['native country', 'count'] 
    
    merged_rich_country = pd.merge(country_count, rich_country_count, on='native country', suffixes = ('-pop.', '-rich-pop.'))

    num_country_pop = merged_rich_country.value_counts().count()
    for i in range(num_country_pop):
        country_name = merged_rich_country.iloc[i,0]#.to_string()
        percente_pop_rich =  (merged_rich_country.iloc[i,2] / merged_rich_country.iloc[i,1]) * 100
        rate_rich.loc[i,'native-country'] = country_name
        rate_rich.loc[i,'rich-rate'] = percente_pop_rich
        

    print(type(rate_rich))
    position = 0
    count = 0
    position_highest_ = 0
    for i in range(rate_rich['rich-rate'].count()):
        highest_rate = rate_rich.loc[i,'rich-rate']
        if position > highest_rate:
            count = count + 1
        elif position == highest_rate:
            count = count + 1
        else:
            position = highest_rate 
            position_highest_ = count
            count = count + 1
    # print(position, count, position_highest_)
    highest_earning_country = rate_rich.loc[position_highest_,'native-country']
    # print(highest_earning_country)
    highest_earning_country_percentage = rate_rich.loc[position_highest_, 'rich-rate'].round(1)
    # print(highest_earning_country_percentage)


    # # Identify the most popular occupation for those who earn >50K in India.
    pop_occupation = df[['occupation', 'salary', 'native-country']]
    pop_occupation = pop_occupation.loc[(pop_occupation['native-country'] == 'India') & (pop_occupation['salary'] == '>50K')]
    pop_occupation_count = pop_occupation['occupation'].value_counts().reset_index()
    pop_occupation_count.columns = ['occupation', 'count'] # Test to see if this line is needed 
    occupation_counters = pop_occupation.value_counts()
    position = 0
    count = 0
    position_highest_ = 0
    for i in range(occupation_counters.count()):
        indicator = occupation_counters.iloc[i]
        if position > indicator:
            count = count + 1
        elif position == indicator:
            count = count + 1
        else:
            position = indicator 
            position_highest_ = count
            count = count + 1

    top_IN_occupation = pop_occupation_count.loc[position_highest_,'occupation']#.to_string()
    #print(top_IN_occupation[:1])
    # # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
