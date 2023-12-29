import pandas as pd
import numpy as np

date_list = ["2017-12-31", "2018-12-31", "2019-12-31", "2020-12-31", "2021-12-31", "2022-12-31"]

def cal_ratio(ratio_name, sheet: pd.DataFrame) -> list:
    ratios = [0,0,0,0,0,0]
    ratios = np.array(ratios)

    net_income = sheet.loc[sheet.iloc[:, 0].str.strip() == '净利润',date_list]
    net_income = np.array(net_income)

    net_sales_revenue = sheet.loc[sheet.iloc[:, 0].str.strip() == '营业总收入',date_list]
    net_sales_revenue = np.array(net_sales_revenue)

    if ratio_name == 'ROE':
        se = sheet.loc[sheet.iloc[:, 0].str.strip().isin(["股东权益","股东权益合计"]),date_list]
        se = np.array(se)
        ratios = net_income / se
        
    elif ratio_name == 'ROA':
        ta = sheet.loc[sheet.iloc[:, 0].str.strip().isin(["资产总计","总资产"]),date_list]
        ta = np.array(ta)
        ratios = net_income / ta
         
    elif ratio_name == 'Gross profit percentage':
        gross_profit = sheet.loc[sheet.iloc[:, 0].str.strip() == '营业利润',date_list]
        gross_profit = np.array(gross_profit)
        ratios = gross_profit / net_sales_revenue
    elif ratio_name == 'Net profit margin':
        ratios = net_income / net_sales_revenue
         
    elif ratio_name == 'EPS':
        # directly use eps provided by the sheet
        ratios = sheet.loc[sheet.iloc[:, 0].str.strip() == 'EPS(基本)',date_list]
        ratios = np.array(ratios)
         
    elif ratio_name == 'Quality of Income':
        cashflows_from_opera = sheet.loc[sheet.iloc[:, 0].str.strip().isin([
            "经营活动现金流量",
            "经营活动现金净流量"
        ]),date_list]
        cashflows_from_opera = np.array(cashflows_from_opera)
        ratios = cashflows_from_opera / net_income
    elif ratio_name == 'Total asset turnover ratio':
        ta = sheet.loc[sheet.iloc[:, 0].str.strip().isin(["资产总计","总资产"]),date_list]
        # cal average ta, first year use itself,the rest use average of last 2 years
        ta = np.array(ta).flatten()
        for i in range(1,6):
            ta[i] = (ta[i-1] + ta[i]) / 2
        ratios = net_sales_revenue / ta
    elif ratio_name == 'Fixed asset turnover ratio':
        fixed_assets = sheet.loc[sheet.iloc[:, 0].str.strip() == '固定资产',date_list]
        fixed_assets = np.array(fixed_assets).flatten()
        for i in range(1,6):
            fixed_assets[i] = (fixed_assets[i-1] + fixed_assets[i]) / 2
        ratios = net_sales_revenue / fixed_assets
    elif ratio_name == 'Receivable turnover ratio':
        pass
    elif ratio_name == 'Inventory turnover ratio':
        pass
    elif ratio_name == 'Current ratio':
        current_assets = sheet.loc[sheet.iloc[:, 0].str.strip().isin([
            "流动资产",
            "流动资产合计"
        ]),date_list]
        current_liabilities = sheet.loc[sheet.iloc[:, 0].str.strip().isin([
            "流动负债",
            "流动负债合计"
        ]),date_list]
        current_assets = np.array(current_assets)
        current_liabilities = np.array(current_liabilities)
        ratios = current_assets / current_liabilities
    elif ratio_name == 'Quick ratio':
        marketable_securities = sheet.loc[sheet.iloc[:, 0].str.startswith("Marketable Securities"),date_list]
        marketable_securities = np.array(marketable_securities)        
        receivables = sheet.loc[sheet.iloc[:, 0].str.startswith("Net Accounts Receivable"),date_list]
        receivables = np.array(receivables)
        cash = sheet.loc[sheet.iloc[:, 0].str.strip() == 'Cash & Cash Equivalents',date_list]
        cash = np.array(cash)
        current_liabilities = sheet.loc[sheet.iloc[:, 0].str.strip() == '流动负债',date_list]
        current_liabilities = np.array(current_liabilities)
        ratios = (marketable_securities + receivables + cash) / current_liabilities
        # set nan to 0
        for i in range(6):
            if np.isnan(ratios[0][i]):
                ratios[0][i] = 0
    elif ratio_name == 'Cash ratio':
        cash = sheet.loc[sheet.iloc[:, 0].str.strip() == 'Cash & Cash Equivalents',date_list]
        cash = np.array(cash)
        current_liabilities = sheet.loc[sheet.iloc[:, 0].str.strip() == '流动负债',date_list]
        current_liabilities = np.array(current_liabilities)
        ratios = cash / current_liabilities
    elif ratio_name == 'Times interest earned ratio':
        interest_expense = sheet.loc[sheet.iloc[:, 0].str.strip() == 'Interest Expense',date_list]
        interest_expense = np.array(interest_expense)
        income_tax_expense = sheet.loc[sheet.iloc[:, 0].str.strip() == 'Income Tax Expense',date_list]
        income_tax_expense = np.array(income_tax_expense)
        ratios = (net_income + interest_expense + income_tax_expense) / interest_expense
    elif ratio_name == 'Cash coverage ratio':
        pass
    elif ratio_name == 'Debt-to-equity ratio':
        total_liabilities = sheet.loc[sheet.iloc[:, 0].str.strip().isin([
            "负债合计",
            "总负债"
        ]),date_list]
        total_equity = sheet.loc[sheet.iloc[:, 0].str.strip().isin([
            "股东权益",
            "股东权益合计"
        ]),date_list]
        total_liabilities = np.array(total_liabilities)
        total_equity = np.array(total_equity)
        ratios = total_liabilities / total_equity
    elif ratio_name == 'P_E ratio':
        market_price = sheet.loc[sheet.iloc[:, 0].str.startswith("Market Price per Share"),date_list]
        market_price = np.array(market_price)
        eps = sheet.loc[sheet.iloc[:, 0].str.strip() == 'EPS(基本)',date_list]
        eps = np.array(eps)
        ratios = market_price / eps

    ratios = ratios.flatten().tolist()

    return ratios

