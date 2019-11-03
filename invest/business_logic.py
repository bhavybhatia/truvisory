from math import sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from operator import mul, add
import gc
import quandl
from .models import *
quandl.ApiConfig.api_key = "GtnywiP1rsMyzzyy6bDz"


class Logic:

    def __init__(self):

        self.user = users.objects.get(id=1)
        self.inc = income.objects.get(id=1)
        self.exp = expenses.objects.get(id=1)
        self.inc = income.objects.get(id=1)
        self.port = portfolio.objects.get(id=1)
        self.otg = OTG.objects.get(id=1)
        self.lfg = LFG.objects.get(id=1)
        self.income_g = Income_Goal.objects.get(id=1)

        self.MRRR = 0
        self.net_cash_flow = []

    def MRRR_Cal(self):

        RRRs = [x * 0.001 for x in range(50, 100000)]

        for RRR in RRRs:

            client = pd.DataFrame({'Age':[self.user.age, self.user.retire, 85], 'Year':[2017, 2017+(self.user.retire-self.user.age), 2017+(85-self.user.age)]})
            client.index = ['Age', 'Expected Retirement', 'Life Expectancy']
            income = pd.DataFrame({'Monthly':[self.inc.sal_and_bonus/12, self.inc.rent/12, self.inc.business/12, self.inc.other/12], 'Yearly':[self.inc.sal_and_bonus, self.inc.rent, self.inc.business, self.inc.other],
                                   'Income End':[self.inc.sal_ends, self.inc.rent_ends, self.inc.business_ends, self.inc.other_ends], 'Growth':[self.inc.exp_sal_growth_in_per, self.inc.exp_growth, self.inc.business_growth, self.inc.other_growth]})
            #income.index = ['Salary', 'Rent', 'Business', 'Other']
            expenses = pd.DataFrame({'Monthly':[exp.regular/12, exp.uti/12, exp.grocery/12, exp.mon_leisure/12, exp.me/12, exp.ds/12], 'Yearly':[exp.regular, exp.uti, exp.grocery, exp.mon_leisure, exp.me, exp.ds],
                                    'Expense End':[exp.regular_ends, exp.uti_ends, exp.grocery_ends, exp.leisure_ends, exp.me_ends, exp.ds_ends], 'Inflation':[exp.exp_ing_reg, exp.exp_inf_uti, exp.exp_inf_groc, exp.exp_les_inf, exp.me_inf, exp.exp_ds_inf]})
            #expenses.index = ['Regular', 'Utilities', 'Grocery', 'Leisure', 'Medical', 'Domestic Staff']
            liabilities = pd.DataFrame({'Monthly':[], 'Yearly':[exp.emi1, exp.emi2], 'End':[exp.emi1_end, exp.emi2_end]})
            #liabilities.index = ['Home Loan', 'Car Loan']
            assets = pd.DataFrame({'Risk':['Market', 'Market'],
                                 'Market Value':[port.equity, port.mutual]})
            #assets.index = ['House', 'Equity Shares', 'Mutual Funds', 'Gold']
            one_time_goals = pd.DataFrame({'Year':[otg.g1_year, otg.g2_year, otg.g3_year, otg.g4_year, otg.g5_year],
                                            'Cost':[otg.g1_cost, otg.g2_cost, otg.g3_cost, otg.g4_cost, otg.g5_cost],
                                            'Inflation':[otg.g1_inf, otg.g2_inf, otg.g3_inf, otg.g4_inf, otg.g5_inf]})
            # one_time_goals.index = ['Second House', 'Higher education', 'Higher education', 'Wedding', 'Wedding']
            recurring_goals = pd.DataFrame({'Cost':[lfg.lg1_cost], 'Start':[lfg.lg1_start], 'End':[lfg.lg1_end],
                                            'Inflation':[lfg.lg1_inf]})
            # recurring_goals.index = ['Vacation']
            low_freq_goals = pd.DataFrame({'Cost':[lfg.lg2_cost], 'Start':[lfg.lg2_start], 'Frequency':[lfg.lg2_freq],
                                          'End':[lfg.lg2_end], 'Inflation':[lfg.lg2_inf]})
            # low_freq_goals.index = ['Car']
            goal_income = pd.DataFrame({'Income':[income_g.i1_income], 'Start':[income_g.i1_start], 'End':[income_g.i1_end], 'Inflation':[income_g.i1_inf]})
            # goal_income.index = ['Second House Rent']

            start = client[client.index=='Age']['Year'].values[0]
            end = client[client.index=='Life Expectancy']['Year'].values[0]
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
                    print(RRR, current)
                    fail = True
                    break

                if not fail:
                    net_cash_flow.append(net_income + initial_inv)

            if not fail:
                self.MRRR = RRR
                break

        return 0

# Net cash flow

    def Cash_Flow(self):

        RRR = self.MRRR

        client = pd.DataFrame({'Age':[self.user.age, self.user.retire, 85], 'Year':[2017, 2017+(self.user.retire-self.user.age), 2017+(85-self.user.age)]})
        client.index = ['Age', 'Expected Retirement', 'Life Expectancy']
        income = pd.DataFrame({'Monthly':[inc.sal_and_bonus/12, inc.rent/12, inc.business/12, inc.other/12], 'Yearly':[inc.sal_and_bonus, inc.rent, inc.business, inc.other],
                               'Income End':[inc.sal_ends, inc.rent_ends, inc.business_ends, inc.other_ends], 'Growth':[inc.exp_sal_growth_in_per, inc.exp_growth, inc.business_growth, inc.other_growth]})
        #income.index = ['Salary', 'Rent', 'Business', 'Other']
        expenses = pd.DataFrame({'Monthly':[exp.regular/12, exp.uti/12, exp.grocery/12, exp.mon_leisure/12, exp.me/12, exp.ds/12], 'Yearly':[exp.regular, exp.uti, exp.grocery, exp.mon_leisure, exp.me, exp.ds],
                                'Expense End':[exp.regular_ends, exp.uti_ends, exp.grocery_ends, exp.leisure_ends, exp.me_ends, exp.ds_ends], 'Inflation':[exp.exp_ing_reg, exp.exp_inf_uti, exp.exp_inf_groc, exp.exp_les_inf, exp.me_inf, exp.exp_ds_inf]})
        #expenses.index = ['Regular', 'Utilities', 'Grocery', 'Leisure', 'Medical', 'Domestic Staff']
        liabilities = pd.DataFrame({'Monthly':[], 'Yearly':[exp.emi1, exp.emi2], 'End':[exp.emi1_end, exp.emi2_end]})
        #liabilities.index = ['Home Loan', 'Car Loan']
        assets = pd.DataFrame({'Risk':['Market', 'Market'],
                             'Market Value':[port.equity, port.mutual]})
        #assets.index = ['House', 'Equity Shares', 'Mutual Funds', 'Gold']
        one_time_goals = pd.DataFrame({'Year':[otg.g1_year, otg.g2_year, otg.g3_year, otg.g4_year, otg.g5_year],
                                        'Cost':[otg.g1_cost, otg.g2_cost, otg.g3_cost, otg.g4_cost, otg.g5_cost],
                                        'Inflation':[otg.g1_inf, otg.g2_inf, otg.g3_inf, otg.g4_inf, otg.g5_inf]})
        # one_time_goals.index = ['Second House', 'Higher education', 'Higher education', 'Wedding', 'Wedding']
        recurring_goals = pd.DataFrame({'Cost':[lfg.lg1_cost], 'Start':[lfg.lg1_start], 'End':[lfg.lg1_end],
                                        'Inflation':[lfg.lg1_inf]})
        # recurring_goals.index = ['Vacation']
        low_freq_goals = pd.DataFrame({'Cost':[lfg.lg2_cost], 'Start':[lfg.lg2_start], 'Frequency':[lfg.lg2_freq],
                                      'End':[lfg.lg2_end], 'Inflation':[lfg.lg2_inf]})
        # low_freq_goals.index = ['Car']
        goal_income = pd.DataFrame({'Income':[income_g.i1_income], 'Start':[income_g.i1_start], 'End':[income_g.i1_end], 'Inflation':[income_g.i1_inf]})
        # goal_income.index = ['Second House Rent']

        start = client[client.index=='Age']['Year'].values[0]
        end = client[client.index=='Life Expectancy']['Year'].values[0]
        incomes = []
        exps = []
        initial_invs = []

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

            self.net_cash_flow.append(net_income + initial_inv)

            plt.figure(figsize=(15, 8))
            plt.plot(net_cash_flow)
            plt.grid()
            plt.title('Cash Flow Net Worth over time')
            plt.savefig('cash_flow.png')

            return 0


    def Mutual_Fund(self):

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
            if annualized_returns_decade[key] > self.MRRR:
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
        client = pd.DataFrame({'Age':[self.user.age, self.user.retire, 85], 'Year':[2017, 2017+(self.user.retire-self.user.age), 2017+(85-self.user.age)]})
        client.index = ['Age', 'Expected Retirement', 'Life Expectancy']
        income = pd.DataFrame({'Monthly':[inc.sal_and_bonus/12, inc.rent/12, inc.business/12, inc.other/12], 'Yearly':[inc.sal_and_bonus, inc.rent, inc.business, inc.other],
                               'Income End':[inc.sal_ends, inc.rent_ends, inc.business_ends, inc.other_ends], 'Growth':[inc.exp_sal_growth_in_per, inc.exp_growth, inc.business_growth, inc.other_growth]})
        #income.index = ['Salary', 'Rent', 'Business', 'Other']
        expenses = pd.DataFrame({'Monthly':[exp.regular/12, exp.uti/12, exp.grocery/12, exp.mon_leisure/12, exp.me/12, exp.ds/12], 'Yearly':[exp.regular, exp.uti, exp.grocery, exp.mon_leisure, exp.me, exp.ds],
                                'Expense End':[exp.regular_ends, exp.uti_ends, exp.grocery_ends, exp.leisure_ends, exp.me_ends, exp.ds_ends], 'Inflation':[exp.exp_ing_reg, exp.exp_inf_uti, exp.exp_inf_groc, exp.exp_les_inf, exp.me_inf, exp.exp_ds_inf]})
        #expenses.index = ['Regular', 'Utilities', 'Grocery', 'Leisure', 'Medical', 'Domestic Staff']
        liabilities = pd.DataFrame({'Monthly':[], 'Yearly':[exp.emi1, exp.emi2], 'End':[exp.emi1_end, exp.emi2_end]})
        #liabilities.index = ['Home Loan', 'Car Loan']
        assets = pd.DataFrame({'Risk':['Market', 'Market'],
                             'Market Value':[port.equity, port.mutual]})
        #assets.index = ['House', 'Equity Shares', 'Mutual Funds', 'Gold']
        one_time_goals = pd.DataFrame({'Year':[otg.g1_year, otg.g2_year, otg.g3_year, otg.g4_year, otg.g5_year],
                                        'Cost':[otg.g1_cost, otg.g2_cost, otg.g3_cost, otg.g4_cost, otg.g5_cost],
                                        'Inflation':[otg.g1_inf, otg.g2_inf, otg.g3_inf, otg.g4_inf, otg.g5_inf]})
        # one_time_goals.index = ['Second House', 'Higher education', 'Higher education', 'Wedding', 'Wedding']
        recurring_goals = pd.DataFrame({'Cost':[lfg.lg1_cost], 'Start':[lfg.lg1_start], 'End':[lfg.lg1_end],
                                        'Inflation':[lfg.lg1_inf]})
        # recurring_goals.index = ['Vacation']
        low_freq_goals = pd.DataFrame({'Cost':[lfg.lg2_cost], 'Start':[lfg.lg2_start], 'Frequency':[lfg.lg2_freq],
                                      'End':[lfg.lg2_end], 'Inflation':[lfg.lg2_inf]})
        # low_freq_goals.index = ['Car']
        goal_income = pd.DataFrame({'Income':[income_g.i1_income], 'Start':[income_g.i1_start], 'End':[income_g.i1_end], 'Inflation':[income_g.i1_inf]})
        # goal_income.index = ['Second House Rent']

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
        plt.plot(self.net_cash_flow)
        plt.plot(new_net_cash_flow)
        plt.grid()
        plt.legend(['Minimum RRR', 'Best RRR'])
        plt.title('Cash Flow Net Worth over time - Min RRR and Best RRR')
        plt.savefig('MinVsBest.png')

        return 0
