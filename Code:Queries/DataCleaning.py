import pandas as pd

#Load the datasets
df_rates = pd.read_csv("/Users/atimil/Documents/EconomicAnalysis/ASEAN_Macro_Percent_Change.csv")

df_macro = pd.read_csv("/Users/atimil/Documents/EconomicAnalysis/ASEAN_Macro_Absolute_Values.csv")

#Drop last column and last 2 rows due to blank cells

df_rates.drop(df_rates.columns[-1], axis=1, inplace=True)
df_rates.drop(df_rates.index[-2:], inplace = True)


df_macro.drop(df_macro.columns[-1], axis=1, inplace=True)
df_macro.drop(df_macro.index[-2:], inplace = True)

#Drop rows regarding unemployment rate from df_macro, as it is in df_rates already
df_macro = df_macro[df_macro['Subject Descriptor'] != 'Unemployment rate']

#Filter Employment columns for now

df_rates = df_rates[df_rates['Subject Descriptor'] != 'Employment']
df_macro = df_macro[df_macro['Subject Descriptor'] != 'Employment']

#Use indicators to make merge process easier

def create_indicator_column(row):
    if "Gross domestic product, constant prices" in row['Subject Descriptor']:
        return 'GDP_Real_Growth'
    elif 'Inflation, average consumer prices' in row['Subject Descriptor']:
        return 'Avg_Inflation'
    elif 'Inflation, end of period consumer prices' in row['Subject Descriptor']:
        return 'EOP_Inflation'
    elif 'Unemployment rate' in row['Subject Descriptor']:
        return 'Unemployment_Rate'
    elif 'Gross domestic product, current prices' in row['Subject Descriptor']:
        if 'U.S. dollars' in row['Units']:
            return 'Current_USD_GDP'
        elif 'Purchasing power parity' in row['Units']:
            return 'GDP_PPP'
    elif 'Gross domestic product per capita' in row['Subject Descriptor']:
        return 'GDP_Per_Capita_PPP'
    elif 'Employment' in row['Subject Descriptor']:
        return 'Employment_Millions'
    elif 'Population' in row['Subject Descriptor']:
        return 'Population_Millions'
    else:
        return 'Other'

#Apply above function to the dataframes

df_rates['Economic_Indicator'] = df_rates.apply(create_indicator_column, axis = 1)
df_macro['Economic_Indicator'] = df_macro.apply(create_indicator_column, axis = 1)

print(df_rates.columns)
print(df_macro.columns)

year_columns = [str(year) for year in range(2014, 2023)]

# #Melt Data Frames

df_rates_melt = df_rates.melt( id_vars = ['Country', 'Economic_Indicator'], value_vars= year_columns, var_name = 'Year', value_name = 'Value')
df_macro_melt = df_macro.melt( id_vars = ['Country', 'Economic_Indicator'], value_vars = year_columns, var_name = 'Year', value_name = 'Value')


#See if any columns need to be converted to numeric

print(df_rates_melt.dtypes)
print(df_macro_melt.dtypes)


#Convert Year to numeric for future calculations
df_rates_melt['Year'] = pd.to_numeric(df_rates_melt['Year'], errors= 'coerce')
df_macro_melt['Year'] = pd.to_numeric(df_macro_melt['Year'], errors= 'coerce')

#Check for Nulls - Clear
print(df_rates_melt.isnull().sum())
print(df_macro_melt.isnull().sum())

#get rid of the commas for df_macro_melt or pandas will be unable to convert tp numeric
df_macro_melt['Value'] = df_macro_melt['Value'].str.replace(',', '', regex = False)

#Convert Value column to numeric
df_rates_melt['Value'] = pd.to_numeric(df_rates_melt['Value'], errors= 'coerce')
df_macro_melt['Value'] = pd.to_numeric(df_macro_melt['Value'], errors= 'coerce')

#Check for nulls

print(df_rates_melt.isnull().sum())
print(df_macro_melt.isnull().sum())


# Calculate employment
# subset unemployment data

unemployment_data = df_rates_melt[df_rates_melt['Economic_Indicator'] == 'Unemployment_Rate'].copy()

#Calculate Employment Rate
unemployment_data['Value'] = 100 - unemployment_data['Value']
unemployment_data['Economic_Indicator'] = 'Employment_Rate'

#Concatenate back to df_macro_melt

df_rates_melt = pd.concat([df_rates_melt, unemployment_data], ignore_index = True)

#Sort by Country and Year
df_rates_melt = df_rates_melt.sort_values(by= ['Country', 'Year'], ascending= [True, True])
df_rates_melt = df_rates_melt.reset_index(drop=True)


#Final check
print(df_macro_melt.head(15))
print(df_rates_melt.head(15))

#Convert to csv

df_macro_melt.to_csv('Macro_Economic.csv', index = False)
df_rates_melt.to_csv('Rates_Economic.csv', index = False)








