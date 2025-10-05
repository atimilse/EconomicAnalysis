import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

#Load in cleaned datasets

df_rates = pd.read_csv('/Users/atimil/PycharmProjects/EconomicAnalysis/EconomicAnalysis/CleanedDatasets/Rates_Economic.csv')
df_macro = pd.read_csv('/Users/atimil/PycharmProjects/EconomicAnalysis/EconomicAnalysis/CleanedDatasets/Macro_Economic.csv')

# Create a dataframe with only Inflation, GDP per Capita, and Unemployment Rate

df_rates_subset = df_rates[(df_rates['Country'].isin(['Indonesia', 'Malaysia', 'Philippines']))
                           & (df_rates['Economic_Indicator'].isin( ['Avg_Inflation', 'Unemployment_Rate']))]

df_macro_subset = df_macro[(df_macro['Country'].isin(['Indonesia', 'Malaysia', 'Philippines']))
                           & (df_macro['Economic_Indicator'] == 'GDP_Per_Capita_PPP')]

df_forecasts = pd.concat([df_rates_subset, df_macro_subset], axis = 0, ignore_index= True)

#Change year to datetime

df_grouped = df_forecasts.groupby(['Country','Economic_Indicator'])

#Create empty results list

results = []

#For loop

for (country, indicator), grouped_df in df_grouped:

    #Checking what is being inputted into the loop

    print(f"Now analyzing {indicator} for {country}")

    # X and Y

    X = grouped_df[['Year']]
    y = grouped_df['Value']

    #Fit model

    lr = LinearRegression()
    lr.fit(X,y)

    #Predictions for existing years

    grouped_df['Predicted'] = lr.predict(X)

    #Predictions for the next 3 years
    recent_year = grouped_df['Year'].max()
    future_years = pd.DataFrame({'Year': range(recent_year + 1, recent_year + 5)})
    future_predictions = lr.predict(future_years)

    #Format dataframe for future predictions
    df_future = pd.DataFrame({'Year' : future_years['Year'], 'Value' : future_predictions, 'Country' : country, 'Economic_Indicator' : indicator, 'Type': 'Prediction', 'Predicted' : future_predictions})

    #Rename Type column
    grouped_df['Type'] = 'Actual'

    #Combine historical and actual data

    combined_df = pd.concat([grouped_df[['Year', 'Value', 'Economic_Indicator', 'Type', 'Country']], df_future], ignore_index=True)

    results.append(combined_df)

#Concatenate results
df_linear_forecasts = pd.concat(results, ignore_index = True)

#Export as csv

df_linear_forecasts.to_csv('LinearPredictions.csv', index = False)

#Plot

df_linear_forecasts['Year'] = pd.to_datetime(df_linear_forecasts ['Year'], format = '%Y')
visual = sns.FacetGrid(df_linear_forecasts, row = 'Country', col = 'Economic_Indicator', hue = 'Type', sharey = False, height = 3, aspect = 1.5)
visual.map(plt.plot, 'Year', 'Value', marker = 'o').add_legend()

visual.set_titles(row_template= '{row_name}', col_template= '{col_name}')
plt.subplots_adjust(top = 0.9)
visual.figure.suptitle('Forecasts for Indicators (Actual vs Predicted)')
plt.show()


