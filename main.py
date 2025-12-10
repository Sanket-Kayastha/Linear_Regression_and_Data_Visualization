import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


data = pd.read_csv("cost_revenue_dirty.csv")
# print(data.shape)
# # print(data.tail())
# # print(data.info())
# print(f"If there is any NAN value {data.isna().values.any()}")
# print(f"there is any duplicate value {data.duplicated().values.any()}")
# duplicate_row = data[data.duplicated()]
# print(f"Duplicate row in data {duplicate_row}")
# print(data.info())

char_to_remove = [',','$']
columns_to_remove = ['USD_Production_Budget', 
                    'USD_Worldwide_Gross',
                    'USD_Domestic_Gross']

for col in columns_to_remove:
    for char in char_to_remove:
        data[col] = data[col].astype(str).str.replace(char, "")

    data[col] = pd.to_numeric(data[col])   

# print(data.head())

data.Release_Date = pd.to_datetime(data.Release_Date)
# print(data.head())
# print(data.info())
# print(data.describe())
# print(data[data.USD_Production_Budget == 1100.00])

# zero_domestic = data[data.USD_Domestic_Gross == 0]
# print(f"Number of films that grossed $0 domestically {len(zero_domestic)}")
# print(zero_domestic.sort_values('USD_Production_Budget'))

# zero_worldwide = data[data.USD_Worldwide_Gross == 0]
# print(f"Number of films that grossed $0 worldwide {len(zero_worldwide)}")
# print(zero_worldwide.sort_values('USD_Production_Budget', ascending=False))

# international_release = data.loc[(data.USD_Domestic_Gross == 0) & (data.USD_Worldwide_Gross != 0)]
# print(f"Number of international releases: {len(international_release)}")
# print(international_release.head())

# international_release = data.query('USD_Domestic_Gross==0 and USD_Worldwide_Gross != 0')
# print(f"Number of international releases: {len(international_release)}")
# print(international_release.tail())

scrape_date = pd.Timestamp('2018-5-1')
future_releases = data[data.Release_Date>= scrape_date]
#print(f"Number of unreleased movies: {len(future_releases)}")
# print(future_releases)
data_clean = data.drop(future_releases.index)
# print(data_clean)
money_losing = data_clean.loc[data_clean.USD_Production_Budget > data_clean.USD_Worldwide_Gross]
#print(len(money_losing)/len(data_clean))
#plt.figure(figsize=(8,4), dpi=200)
# with sns.axes_style('darkgrid'):
#     ax = sns.scatterplot(data = data_clean, 
#                          x="USD_Production_Budget", 
#                          y="USD_Worldwide_Gross",
#                          hue='USD_Worldwide_Gross', 
#                          size='USD_Worldwide_Gross')
#     ax.set(ylim=(0,3000000000), 
#            xlim=(0,450000000),
#              ylabel='Revenue in $ billions',
#                xlabel='Budget in $100 millions')

# with sns.axes_style("darkgrid"):
#     ax = sns.scatterplot(data=data_clean,
#                          x='Release_Date',
#                          y='USD_Production_Budget',
#                          hue='USD_Worldwide_Gross',
#                          size='USD_Worldwide_Gross')
    
#     ax.set(ylim=(0,450000000),
#            xlim=(data_clean.Release_Date.min(),
#                  data_clean.Release_Date.max()),
#                  xlabel='Year',
#                  ylabel='Budget in $100 millions')

dt_index = pd.DatetimeIndex(data_clean.Release_Date)
years = dt_index.year

decades = years//10
decades=decades*10
data_clean['Decade'] = decades

old_films = data_clean[data_clean.Decade <= 1960]
new_films = data_clean[data_clean.Decade > 1960]

# print(old_films.describe())
# with sns.axes_style("whitegrid"):
#     sns.regplot(data=old_films,
#              x='USD_Production_Budget',
#                y="USD_Worldwide_Gross",
#                scatter_kws={'alpha':0.4},
#                line_kws={'color':'black'})

# with sns.axes_style('darkgrid'):
#     ax = sns.regplot(data=new_films,
#                      x='USD_Production_Budget',
#                      y='USD_Worldwide_Gross',
#                      color = "#2f4b7c",
#                      scatter_kws= {'alpha':0.3},
#                      line_kws={'color': '#ff7c43'})
#     ax.set(ylim=(0, 3000000000),
#            xlim = (0, 450000000),
#            ylabel = 'Revenue in $ billions',
#            xlabel = "Budget in $100 millions")

regression = LinearRegression()
X = pd.DataFrame(new_films, columns=['USD_Production_Budget'])
y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])
# print(regression.fit(X, y))
# print(regression.score(X,y))
# regression.fit(X,y)
# print(f"The slope coefficient is: {regression.coef_[0]}")
# print(f"The intercept is: {regression.intercept_[0]}")
# print(f"The r-squared is: {regression.score(X,y)}")

budget = 350000000
revenue_estimate = regression.intercept_[0]+regression.coef_[0,0]*budget
revenue_estimate = round(revenue_estimate, -6)
print(f"The estimated revenue for a $350 film is around ${revenue_estimate:.10}.")





#plt.show()