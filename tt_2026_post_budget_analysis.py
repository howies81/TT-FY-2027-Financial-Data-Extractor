import pandas as pd, numpy as np
import pathlib
from pathlib import Path
from datetime import datetime

# Define the Ministry of Finance official 2026 baseline benchmarks
GOVT_GAS_BENCHMARK = 4.25  # US$ / MMBtu
GOVT_OIL_BENCHMARK = 73.25  # US$ / bbl

prod_csv_path = Path.cwd().joinpath("TT_Economy_Data/Output - Production, Exports and Local Sales of Energy Commodities (Monthly).csv")
energy_prices_path = Path.cwd().joinpath("TT_Economy_Data/Energy Prices (Monthly).csv")
hsf_path = Path.cwd().joinpath("TT_Economy_Data/Fiscal - Financing (Monthly).csv")
forex_path = Path.cwd().joinpath("TT_Economy_Data/Exchange Rates (Monthly).csv")
rev_path = Path.cwd().joinpath("TT_Economy_Data/Fiscal - Revenue (Monthly).csv")

energy_prod_df = pd.read_csv(prod_csv_path, skiprows=2)
monthly_energy_prices_df = pd.read_csv(energy_prices_path, skiprows=2)
hsf_path_df = pd.read_csv(hsf_path, skiprows=2)
forex_path_df = pd.read_csv(forex_path, skiprows=2)
rev_path_df = pd.read_csv(rev_path, skiprows=2)
# print(energy_prod_df.columns)
# print("\n\n")
#print(monthly_energy_prices_df.columns)

energy_prod_df_clean = energy_prod_df[['Date', 'Crude Oil Production Daily Average (000s Barrels)',
       'Crude Oil Production (000 Barrels)',
       'Crude Oil Exports (000s Barrels)', 'Natural Gas Production (mmcf/d)',]]

monthly_energy_prices_df_clean = monthly_energy_prices_df[['Date', 'WTI Crude Oil Price (US$/bbl)',
       'Henry Hub Natural Gas Price (US$/mmbtu)',]]

hsf_path_clean_df = hsf_path_df[['Date', 'Withdrawals from HSF (TT$Mn)']]
forex_path_clean_df = forex_path_df[['Date', 'USD Buying Rate', 'USD Selling Rate']]
rev_path_clean_df = rev_path_df[['Date', 'Central Government Total Revenue (TT$Mn)', 'Central Government Oil Revenue (TT$Mn)', 'Central Government Non-Oil Revenue (TT$Mn)', 'Central Government Energy Revenue (TT$Mn)', 'Central Government Non-Energy Revenue (TT$Mn)']]

energy_rev_df = pd.merge(energy_prod_df_clean, monthly_energy_prices_df_clean, how="left", on="Date")
energy_rev_df = pd.merge(energy_rev_df, hsf_path_clean_df, how="left", on="Date")
energy_rev_df = pd.merge(energy_rev_df, forex_path_clean_df, how="left", on="Date")
energy_rev_df = pd.merge(energy_rev_df, rev_path_clean_df, how="left", on="Date")
# print(energy_rev_df.columns)
# print(energy_rev_df.head())
energy_rev_df['Date'] = pd.to_datetime(energy_rev_df['Date'], format="%d/%m/%Y")
energy_rev_df = energy_rev_df[energy_rev_df['Date'] > datetime(year=2025, month=11, day=1)]


# print(energy_rev_df.shape)
energy_rev_df = energy_rev_df[energy_rev_df['Crude Oil Exports (000s Barrels)'] != "n.d."]
# print(energy_rev_df.shape)
# print(energy_rev_df.head())
energy_rev_df["Projected Oil Revenue ($US)"] = energy_rev_df['Crude Oil Exports (000s Barrels)'].astype(float) * 1000 * (energy_rev_df['WTI Crude Oil Price (US$/bbl)']).astype(float)
energy_rev_df['Projected Natural Gas Revenue ($US)'] = energy_rev_df['Natural Gas Production (mmcf/d)'].astype(float) * energy_rev_df['Date'].dt.day.astype(float) * 1030 * energy_rev_df['Henry Hub Natural Gas Price (US$/mmbtu)'].astype(float)

energy_rev_df["Oil_Price_Variance"] = (energy_rev_df['WTI Crude Oil Price (US$/bbl)']).astype(float) - GOVT_OIL_BENCHMARK
energy_rev_df["Gas_Price_Variance"] = (energy_rev_df['Henry Hub Natural Gas Price (US$/mmbtu)']).astype(float) - GOVT_GAS_BENCHMARK
# Calculate the gross dollar value of production based on the budget benchmark
# Note: Multiplying by 1000 because your column is scaled in thousands (000s)
energy_rev_df["Budgeted_Oil_Value_USD"] = (
    energy_rev_df["Crude Oil Exports (000s Barrels)"].astype(float) * 1000 * GOVT_OIL_BENCHMARK)
energy_rev_df['Budgeted_Gas_Value_USD'] = (
    energy_rev_df['Natural Gas Production (mmcf/d)'].astype(float) * energy_rev_df['Date'].dt.day.astype(float) * 1030 * GOVT_GAS_BENCHMARK)

# Find the total dollar variance (Windfall vs Deficit) for each month
energy_rev_df["Oil_Revenue_Variance_USD"] = (
    energy_rev_df["Projected Oil Revenue ($US)"] - energy_rev_df["Budgeted_Oil_Value_USD"]
)
energy_rev_df['Gas_Revenue_Variance_USD'] = (
    energy_rev_df['Projected Natural Gas Revenue ($US)'] - energy_rev_df['Budgeted_Gas_Value_USD']
)

energy_rev_df['Total_OG_Variance_USD'] = (
    energy_rev_df['Oil_Revenue_Variance_USD'] + energy_rev_df['Gas_Revenue_Variance_USD']
)

energy_rev_df['Total_OG_Variance_TTD'] = (
    energy_rev_df['Total_OG_Variance_USD'] * energy_rev_df['USD Buying Rate'].astype(float)
)

og_proj_total_tt = round(energy_rev_df['Total_OG_Variance_TTD'].sum(), 2)
og_proj_total_us = round(energy_rev_df['Total_OG_Variance_USD'].sum(), 2)


print(energy_rev_df.columns)
print(energy_rev_df.shape)
print(energy_rev_df.head())
print(og_proj_total_tt)
print(og_proj_total_us)

energy_rev_df.to_csv("Energy_Rev.csv")
