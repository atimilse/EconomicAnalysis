USE EconomicAnalysis;

/* Top 3 Countries with Highest GDP Per Capita */

SELECT TOP 3 Country, Value as GDP_Per_Capita
FROM Macro_Economic
WHERE Economic_Indicator = 'GDP_Per_Capita_PPP' AND Year = 2022
ORDER BY GDP_Per_Capita DESC;

/*Top 3 Countries with Highest Unemployment*/
SELECT TOP 3 Country, Value as Unemployment_Rate
FROM Macro_Economic
WHERE Economic_Indicator = 'Unemployment_Rate' AND Year = 2022
ORDER BY Unemployment_Rate DESC;


/*Top 3 Countries with Most Stable Inflation*/

SELECT TOP 3 Country, Value as Inflation
FROM Rates_Economic
WHERE Economic_Indicator = 'Avg_Inflation' AND Year = 2022
ORDER BY Inflation;

/* Compare GDP Growth Trend for each country over past 5 years */

SELECT Country, AVG(Value)AS Avg_GDP_Growth
FROM Rates_Economic
WHERE Economic_Indicator = 'GDP_Real_Growth'
AND YEAR BETWEEN 2018 AND 2022
GROUP BY Country
ORDER BY Avg_GDP_Growth DESC

/*GDP per Capita Categories(Based on World Bank Thresholds for 2022) */
SELECT Country, Value AS GDP_Per_Capita,
CASE
WHEN Value >= 12695 THEN 'High'
WHEN Value BETWEEN 4096 AND 12695 THEN 'Upper Middle'
WHEN Value BETWEEN 1046 AND 4095 THEN 'Lower Middle'
ELSE 'Low' END AS 'Avg_Standard_of_Living'
FROM Macro_Economic
WHERE Economic_Indicator = 'GDP_Per_Capita_PPP'
AND Year = 2022
ORDER BY GDP_Per_Capita DESC;

/* Countries with Increasing Unemployment Over 3 Years*/

SELECT  DISTINCT r1.Country
FROM Rates_Economic r1
JOIN Rates_Economic r2 ON r1.Country = r2.Country
JOIN Rates_Economic r3 ON r1.Country = r3.Country
WHERE
r1.Economic_Indicator = 'Unemployment_Rate'
AND r2.Economic_Indicator = 'Unemployment_Rate'
AND r3.Economic_Indicator = 'Unemployment_Rate'
AND r1.Year = 2020
AND r2.Year = 2021
AND r3.Year = 2022
AND r1.Value < r2.Value
AND r2.Value < r3.Value;

/* Compare Unemployment and Employment Rates for the past 5 Years */

SELECT 
m.Country, m.Value AS Current_USD_GDP, r.Value as Unemployment_Rate
FROM Macro_Economic m
JOIN Rates_Economic r
ON m.Country = r.Country AND m.Year = r.Year
WHERE
m.Economic_Indicator = 'Current_USD_GDP'
AND r.Economic_Indicator = 'Unemployment_Rate'
AND m.Year = 2022;


/* Employment Rate percent and Category for a year */

SELECT m.Country, m.Value AS Employment_Rate, mm.Value AS Population_in_millions,
CASE
	WHEN m.Value >= 70 THEN 'HIGH'
	WHEN m.Value BETWEEN 50 AND 69 THEN 'MEDIUM'
	ELSE 'LOW'
END AS Employment_Catgeory
FROM Macro_Economic m
JOIN
Macro_Economic mm
ON m.Country = mm.Country AND m.Year = mm.Year
WHERE
m.Economic_Indicator = 'Employment_Rate'
AND mm.Economic_Indicator = 'Population_Millions'
AND m.Year = 2022
ORDER BY m.Value DESC;


/* Employment Rate and GDP Growth*/

SELECT r.Country, r.Value AS GDP_Real_Growth,
m.Value AS Employment_Rate
FROM Rates_Economic r
JOIN Macro_Economic m
ON r.Country = m.Country AND r.Year = m.Year
WHERE
r.Economic_Indicator = 'GDP_Real_Growth'
AND m.Economic_Indicator = 'Employment_Rate'
AND r.year = 2022
ORDER BY r.Country

/*Average Inflation over 5 Years by Country */
SELECT Country, AVG(Value) AS Avg_Inflation_5year
FROM Rates_Economic
WHERE Economic_Indicator = 'Avg_Inflation'
AND Year BETWEEN 2018 AND 2022
GROUP BY Country
ORDER BY Avg_Inflation_5year

/*Inflation Categories for Countries in a Year */

SELECT Country, Value AS Inflation_Average,
CASE
WHEN Value < 2 THEN 'Stable'
WHEN Value BETWEEN 2 AND 5 THEN 'Moderate'
ELSE 'Volatile' END AS Inflation_Category
FROM Rates_Economic
WHERE Economic_Indicator = 'Avg_Inflation'
AND Year = 2022
ORDER BY Inflation_Average;

/*EOP Inflation*/

SELECT Country, Value AS EOP_Inflation,
CASE
WHEN Value < 2 THEN 'Stable'
WHEN Value BETWEEN 2 AND 5 THEN 'Moderate'
ELSE 'Volatile' END AS EOP_Inflation_Category
FROM Rates_Economic
WHERE Economic_Indicator = 'EOP_Inflation'
AND Year = 2022
ORDER BY EOP_Inflation;

/* Population Growth Over 5 years */
SELECT Country, Year, Value as Population
FROM Macro_Economic
WHERE Economic_Indicator = 'Population_Millions'
AND YEAR BETWEEN 2018 AND 2022
ORDER BY Country, Year;
