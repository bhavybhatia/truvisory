from math import sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from operator import mul, add
import quandl
quandl.ApiConfig.api_key = "GtnywiP1rsMyzzyy6bDz"


# Sample dataframes

# func for RRR

RRRs = [x * 0.001 for x in range(5  0, 100000)]

MRRR = 0

for RRR in RRRs:

    # Reset dataframes

    start = client[client.index=='Age']['Year'].values[0]
    # end = client[client.index=='Life Expectancy']['Year'].values[0]
    end = 85
    net_cash_flow = []
    incomes = []
    exps = []
    initial_invs = []
    fail = False

    for current in range(start, end+1):

        # initial_invs.append(initial_inv)
        year_income = income[income['Income End']>=current].Yearly.values.sum()
        income.Yearly = list(map(add, list(map(abs, list(map(mul, list(income.Yearly.values), list(income.Growth.values))))), list(income.Yearly.values)))
        income.Monthly = [elem/12 for elem in list(income.Yearly.values)]
        g_income = goal_income[(goal_income['Start']<=current) & (goal_income['End']>=current)].Income.values.sum()
        year_income += g_income
        goal_income.Income = list(map(add, list(map(abs, list(map(mul, list(goal_income.Income.values), list(goal_income.Inflation))))), list(goal_income.Income.values)))

        incomes.append(year_income)

        year_expenses = expenses[expenses['Expense End']>=current].Yearly.values.sum()
        expenses.Yearly = list(map(add, list(map(abs, list(map(mul, list(expenses.Yearly.values), list(expenses.Inflation.values))))), list(expenses.Yearly.values)))
        expenses.Monthly = [elem/12 for elem in list(expenses.Yearly.values)]
        year_liabilities = liabilities[liabilities['End']>=current].Yearly.values.sum()
        one_time_expense = one_time_goals[one_time_goals['Year']==current].Cost.values.sum()
        one_time_goals.Cost = list(map(add, list(map(mul, list(one_time_goals['Cost']), list(one_time_goals.Inflation.values))), list(one_time_goals.Cost)))
        low_freq_expense_rows = low_freq_goals[(low_freq_goals['Start']<=current) & (low_freq_goals['End']>=current)]
        low_freq_expense = 0
        for index, row in low_freq_expense_rows.iterrows():
            if (current - row['Start']) % row['Frequency'] == 0:
                low_freq_expense += row['Cost']
        freq_expense = recurring_goals[(recurring_goals['Start']<=current) & (recurring_goals['End']>=current)].Cost.values.sum()
        recurring_goals.Cost = list(map(add, list(map(mul, list(recurring_goals['Cost']), list(recurring_goals.Inflation.values))), list(recurring_goals.Cost)))
        year_expenses += year_liabilities + one_time_expense + freq_expense + low_freq_expense

        exps.append(year_expenses)

        net_income = year_income - year_expenses

        if current == start:
            initial_inv = assets[assets.Risk=='Market']['Market Value'].values.sum()
        else:
            initial_inv = net_cash_flow[-1]

        initial_inv *= (1 + RRR) # Check

        if net_income + initial_inv < 0:
            # print(RRR, current)
            fail = True
            break

        if not fail:
            net_cash_flow.append(net_income + initial_inv)

    if not fail:
        MRRR = RRR
        break

# Net cash flow

# Reset data

start = client[client.index=='Age']['Year'].values[0]
end = client[client.index=='Life Expectancy']['Year'].values[0]
net_cash_flow = []
incomes = []
exps = []
initial_invs = []

RRR = MRRR

for current in range(start, end+1):

    if current == start:
        initial_inv = assets[assets.Risk=='Market']['Market Value'].values.sum()
    else:
        initial_inv = net_cash_flow[-1]

    initial_inv *= (1 + RRR/1) # Check

    initial_invs.append(initial_inv)

    year_income = income[income['Income End']>=current].Yearly.values.sum()
    income.Yearly = list(map(add, list(map(abs, list(map(mul, list(income.Yearly.values), list(income.Growth.values))))), list(income.Yearly.values)))
    income.Monthly = [elem/12 for elem in list(income.Yearly.values)]
    g_income = goal_income[(goal_income['Start']<=current) & (goal_income['End']>=current)].Income.values.sum()
    year_income += g_income
    goal_income.Income = list(map(add, list(map(abs, list(map(mul, list(goal_income.Income.values), list(goal_income.Inflation))))), list(goal_income.Income.values)))

    incomes.append(year_income)

    year_expenses = expenses[expenses['Expense End']>=current].Yearly.values.sum()
    expenses.Yearly = list(map(add, list(map(abs, list(map(mul, list(expenses.Yearly.values), list(expenses.Inflation.values))))), list(expenses.Yearly.values)))
    expenses.Monthly = [elem/12 for elem in list(expenses.Yearly.values)]
    year_liabilities = liabilities[liabilities['End']>=current].Yearly.values.sum()
    one_time_expense = one_time_goals[one_time_goals['Year']==current].Cost.values.sum()
    one_time_goals.Cost = list(map(add, list(map(mul, list(one_time_goals['Cost']), list(one_time_goals.Inflation.values))), list(one_time_goals.Cost)))
    low_freq_expense_rows = low_freq_goals[(low_freq_goals['Start']<=current) & (low_freq_goals['End']>=current)]
    low_freq_expense = 0
    for index, row in low_freq_expense_rows.iterrows():
        if (current - row['Start']) % row['Frequency'] == 0:
            low_freq_expense += row['Cost']
    freq_expense = recurring_goals[(recurring_goals['Start']<=current) & (recurring_goals['End']>=current)].Cost.values.sum()
    recurring_goals.Cost = list(map(add, list(map(mul, list(recurring_goals['Cost']), list(recurring_goals.Inflation.values))), list(recurring_goals.Cost)))
    year_expenses += year_liabilities + one_time_expense + freq_expense + low_freq_expense

    exps.append(year_expenses)

    net_income = year_income - year_expenses

    net_cash_flow.append(net_income + initial_inv)

df = pd.DataFrame({'cash_flow':net_cash_flow})
df.index = [i for i in range(start, end+1)]
plt.figure(figsize=(15, 8))
plt.plot(df)
plt.grid()
plt.title('Cash Flow Net Worth over time')
plt.savefig('cash_flow.png')

fund1 = quandl.get("AMFI/104481")
fund2 = quandl.get("AMFI/100546")
fund3 = quandl.get("AMFI/103504")
fund4 = quandl.get("AMFI/102756")
fund5 = quandl.get("AMFI/100639")
fund6 = quandl.get("AMFI/102941")
fund7 = quandl.get("AMFI/100900")
fund8 = quandl.get("AMFI/103234")

funds = [fund1, fund2, fund3, fund4, fund5, fund6, fund7, fund8]

fund_keys = {1:'AMFI/104481', 2:'AMFI/100546', 3:'AMFI/103504', 4:'AMFI/102756', 5:'AMFI/100639',
             6:'AMFI/102941', 7:'AMFI/100900', 8:'AMFI/103234'}

# timestamp from database -> month, year
# annualized return for one fund currently

RFR = 0.06
counter = 1
sharpes = {}
annualized_returns = {}
annualized_returns_decade = {}
monthly_return = {}
for fund in funds:
    current_month = 9
    current_year = 2019
    monthly_returns = []
    for i in range(120):
        current_nav = fund[(fund.index.month==current_month) & (fund.index.year==current_year)].iloc[-1]['Net Asset Value']
        prev_month = current_month-1
        prev_year = current_year
        if prev_month < 1:
            prev_month += 12
            prev_year = current_year-1
        prev_nav = fund[(fund.index.month==prev_month) & (fund.index.year==prev_year)].iloc[-1]['Net Asset Value']
        monthly_returns.append(((current_nav - prev_nav) / prev_nav))
        current_month = prev_month
        current_year = prev_year
        if i==0:
            monthly_return[counter] = ((current_nav - prev_nav) / prev_nav)
    Ns = [2, 3, 5, 10]
    N_sharpe = {}
    N_return = {}
    for N in Ns:
        temp = [elem+1 for elem in monthly_returns][-(12*N):]
        pro = 1
        for elem in temp:
            pro *= elem
        annualized_return = pow(pro, 1/N)-1
        sharpe = (annualized_return - RFR) / (np.std(monthly_returns) * sqrt(12))
        N_sharpe[N] = sharpe
        N_return[N] = annualized_return
        if N==10:
            annualized_returns_decade[counter] = annualized_return
    sharpes[counter] = N_sharpe
    annualized_returns[counter] = N_return
    counter += 1


reco_funds_returns = []
for key in annualized_returns_decade.keys():
    if annualized_returns_decade[key] > RRR:
        reco_funds_returns.append(key)


reco_fund_sharpe = None
sharpe = 0
for key in reco_funds_returns:
    if sharpes[key][10] > sharpe:
        sharpe = sharpes[key][10]
        reco_fund_sharpe = key


plt.figure(figsize=(15, 8))
plt.title('Annualized Returns for all funds: 10 Years')
sns.barplot(x=list(annualized_returns_decade.keys()), y=list(annualized_returns_decade.values()))
plt.savefig('annual_returns.png')


reco_vals = []
for key in reco_funds_returns:
    reco_vals.append(sharpes[key][10])
plt.figure(figsize=(15, 8))
plt.title('Sharpe ratios for recommended funds')
sns.barplot(x=reco_funds_returns, y=reco_vals)
plt.savefig('sharpe.png')


# Reset dataframe

start = client[client.index=='Age']['Year'].values[0]
end = client[client.index=='Life Expectancy']['Year'].values[0]
new_net_cash_flow = []
incomes = []
exps = []
initial_invs = []

RRR = annualized_returns_decade[reco_fund_sharpe]

for current in range(start, end+1):

    if current == start:
        initial_inv = assets[assets.Risk=='Market']['Market Value'].values.sum()
    else:
        initial_inv = new_net_cash_flow[-1]

    initial_inv *= (1 + RRR/1) # Check

    initial_invs.append(initial_inv)

    year_income = income[income['Income End']>=current].Yearly.values.sum()
    income.Yearly = list(map(add, list(map(abs, list(map(mul, list(income.Yearly.values), list(income.Growth.values))))), list(income.Yearly.values)))
    income.Monthly = [elem/12 for elem in list(income.Yearly.values)]
    g_income = goal_income[(goal_income['Start']<=current) & (goal_income['End']>=current)].Income.values.sum()
    year_income += g_income
    goal_income.Income = list(map(add, list(map(abs, list(map(mul, list(goal_income.Income.values), list(goal_income.Inflation))))), list(goal_income.Income.values)))

    incomes.append(year_income)

    year_expenses = expenses[expenses['Expense End']>=current].Yearly.values.sum()
    expenses.Yearly = list(map(add, list(map(abs, list(map(mul, list(expenses.Yearly.values), list(expenses.Inflation.values))))), list(expenses.Yearly.values)))
    expenses.Monthly = [elem/12 for elem in list(expenses.Yearly.values)]
    year_liabilities = liabilities[liabilities['End']>=current].Yearly.values.sum()
    one_time_expense = one_time_goals[one_time_goals['Year']==current].Cost.values.sum()
    one_time_goals.Cost = list(map(add, list(map(mul, list(one_time_goals['Cost']), list(one_time_goals.Inflation.values))), list(one_time_goals.Cost)))
    low_freq_expense_rows = low_freq_goals[(low_freq_goals['Start']<=current) & (low_freq_goals['End']>=current)]
    low_freq_expense = 0
    for index, row in low_freq_expense_rows.iterrows():
        if (current - row['Start']) % row['Frequency'] == 0:
            low_freq_expense += row['Cost']
    freq_expense = recurring_goals[(recurring_goals['Start']<=current) & (recurring_goals['End']>=current)].Cost.values.sum()
    recurring_goals.Cost = list(map(add, list(map(mul, list(recurring_goals['Cost']), list(recurring_goals.Inflation.values))), list(recurring_goals.Cost)))
    year_expenses += year_liabilities + one_time_expense + freq_expense + low_freq_expense

    exps.append(year_expenses)

    net_income = year_income - year_expenses

    new_net_cash_flow.append(net_income + initial_inv)

plt.figure(figsize=(15, 8))
df = pd.DataFrame({'min_cash_flow':net_cash_flow, 'best_cash_flow':new_net_cash_flow})
df.index = [i for i in range(start, end+1)]
plt.plot(df)
plt.grid()
plt.legend(['Minimum RRR', 'Best RRR'])
plt.title('Cash Flow Net Worth over time - Min RRR and Best RRR')
plt.savefig('MinVsBest.png')

plt.figure(figsize=(15, 8))
plt.plot(funds[reco_fund_sharpe])
plt.title('Net Asset Value of ' + fund_keys[reco_fund_sharpe] + ' over time')
plt.grid()
plt.save('nav.png')
