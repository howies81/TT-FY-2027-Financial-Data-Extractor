import openpyxl
from openpyxl.chart import LineChart, Reference, BarChart
from openpyxl.chart.series_factory import SeriesFactory
from openpyxl.chart.axis import ChartLines
from pathlib import Path

nat_gas_file_path = Path.cwd().joinpath("TT_Nat_Gas_Prod_Util_2026.xlsx")
gdp_file_path = Path.cwd().joinpath("GDP_2026_Analysis_Output.xlsx")

nat_gas_wb = openpyxl.load_workbook(nat_gas_file_path)
gdp_ttd_wb = openpyxl.load_workbook(gdp_file_path)

nat_gas_ws = nat_gas_wb["TT_Nat_Gas_Prod"]
if "TT_Nat_Gas_Prod_Copy" not in nat_gas_wb.sheetnames:
    nat_gas_ws_clean = nat_gas_wb.copy_worksheet(nat_gas_ws)
    nat_gas_ws_clean.delete_cols(2)
    nat_gas_ws_clean.delete_cols(6)
else:
    nat_gas_wb.remove(nat_gas_wb["TT_Nat_Gas_Prod_Copy"])
    nat_gas_ws_clean = nat_gas_wb.copy_worksheet(nat_gas_ws)
    nat_gas_ws_clean.delete_cols(2)
    nat_gas_ws_clean.delete_cols(6)


# gdp_ws = gdp_ttd_wb["GDP Const 2012 Prices TTD Mn"]
# gdp_ws_staging = nat_gas_wb.create_sheet(title= "Mfg_GDP_TTD_Data")

# mfg_gdp_row = 4

# # gdp_headers = [gdp_ws.cell(row=1, column=col) for col in range(1, 8)]
# gdp_headers = []
# for col in range(1, 10):
#     if col in [2, 7, 8]:
#         continue
#     else:
#         raw_val = gdp_ws.cell(row= 1, column= col).value
#         gdp_headers.append(raw_val)
# gdp_headers[0] = ""
# gdp_ws_staging.append(gdp_headers)

# # mfg_gdp_data = [gdp_ws.cell(row=mfg_gdp_row, column= col) for col in range(1, 8)]
# mfg_gdp_data = []
# for col in range(1, 10):
#     if col in [2, 7, 8]:
#         continue
#     else:
#         raw_val = gdp_ws.cell(row= mfg_gdp_row, column= col).value
#         mfg_gdp_data.append(raw_val)
# gdp_ws_staging.append(mfg_gdp_data)

# gdp_ttd_wb.close()
# nat_gas_ws_rows = []





nat_gas_chart = BarChart()
nat_prod_chart = LineChart()
nat_gas_chart.x_axis.delete = False
nat_gas_chart.y_axis.delete = False
nat_gas_chart.style = 13
nat_gas_chart.grouping = "stacked"
nat_gas_chart.overlap = 100

nat_prod_chart.y_axis.delete = False
nat_prod_chart.style = 13
nat_prod_chart.y_axis.title = "Gas Production (MMSCF/D)"

nat_gas_chart.title = "T&T Gas Utilisation per sector"
nat_gas_chart.x_axis.title = "Financial Year Period"
nat_gas_chart.y_axis.title = "Gas Volume Allocation (MMSCF/D)"
nat_gas_chart.y_axis.tickLblPos = "nextTo"
nat_gas_chart.y_axis.number_format = '#,###.0'
nat_gas_chart.y_axis.majorGridlines = ChartLines()

if nat_gas_ws_clean is not None:
    # Set Financial Periods X-axis
    # borrow_chart_hsf_data_ref = Reference(ws, min_col=1, max_col= 7, min_row=5, max_row= 5)
    nat_gas_cat_ref = Reference(nat_gas_ws_clean, min_col= 2, max_col= 6, min_row= 1, max_row= 1)
    

    # Ammonia and Methanol data processing
    # nat_gas_ammonia_data_ref = Reference(nat_gas_ws_clean, min_col=1, max_col= 6, min_row=5, max_row= 5)
    # nat_gas_meth_data_ref = Reference(nat_gas_ws_clean, min_col=1, max_col= 6, min_row=6, max_row= 6)
    # nat_gas_pwr_gen_ref = Reference(nat_gas_ws_clean, min_col=1, max_col= 6, min_row=4, max_row= 4)
    # nat_gas_iron_steel_ref = Reference(nat_gas_ws_clean, min_col=1, max_col= 6, min_row=8, max_row= 8)
    # nat_gas_cement_ref = Reference(nat_gas_ws_clean, min_col=1, max_col= 6, min_row=9, max_row= 9)
    # nat_gas_cement_ref = Reference(nat_gas_ws_clean, min_col=1, max_col= 6, min_row=9, max_row= 9)
    nat_gas_refs = []
    for i in range(0, 12):
        nat_gas_refs_temp = Reference(nat_gas_ws_clean, min_col= 1, max_col= 6, min_row=(i + 4), max_row=(i + 4))
        nat_gas_refs.append(nat_gas_refs_temp)

    
    # Add colummns to chart
    for i in range(1, 12):
        nat_gas_chart.add_data(nat_gas_refs[i], titles_from_data= True, from_rows= True)
    # nat_gas_chart.add_data(nat_gas_meth_data_ref, titles_from_data= True, from_rows= True)
    # borrow_chart.add_data(borrow_chart_ext_data_ref, titles_from_data= True, from_rows= True)
    nat_gas_chart.set_categories(nat_gas_cat_ref)

    colors = ["1F77B4", "FF7F0E", "2CA02C", "D62728", "9467BD", "8C564B", 
                   "E377C2", "7F7F7F", "BCBD22", "17BECF", "34495E", "E67E22"]
    # markers = ["circle", "triangle"]
    for i, color_hex in enumerate(colors):
        if i < len(nat_gas_chart.series):
            nat_gas_chart.series[i].graphicalProperties.solidFill = color_hex
            nat_gas_chart.series[i].graphicalProperties.line.solidFill = color_hex

    gas_prod_ref = Reference(nat_gas_ws_clean, min_col=1, max_col=6, min_row=2, max_row=2)
    nat_prod_chart.add_data(gas_prod_ref, titles_from_data=True, from_rows= True)
    # for i, marker in enumerate(markers):
    #     if i < len(nat_gas_chart.series):
    #         nat_gas_chart.series[i].marker.symbol = marker
    #         # nat_gas_chart.series[i].graphicalProperties.line.solidFill = color_hex

    # mfg_gdp_ref = Reference(gdp_ws_staging, min_col= 1, max_col= 6, min_row=2, max_row= 2)
    # gdp_chart.add_data(mfg_gdp_ref, titles_from_data= True, from_rows= True)

    nat_prod_series = nat_prod_chart.series[0]
    nat_prod_series.graphicalProperties.line.solidFill = "2980B9"  # GDP: Deep Blue
    nat_prod_series.graphicalProperties.line.width = 35000
    nat_prod_series.marker.symbol = "square"

    # ==============================================================================
    # (Dual-Axis Combination)
    # ==============================================================================

    nat_prod_chart.y_axis.axId = 300
    nat_prod_chart.y_axis.crosses = "max"
    nat_prod_chart.y_axis.number_format = "#,###"

    # Merge the GDP trend layer cleanly over the underlying Gas allocations
    nat_gas_chart += nat_prod_chart

    if "Downstream Gas Util" not in nat_gas_wb.chartsheets:
        chart_sheet = nat_gas_wb.create_chartsheet(title="Downstream Gas Util")
        chart_sheet.add_chart(nat_gas_chart)
    else:
        nat_gas_wb.remove(nat_gas_wb["Downstream Gas Util"])
        chart_sheet = nat_gas_wb.create_chartsheet(title="Downstream Gas Util")
        chart_sheet.add_chart(nat_gas_chart)

    nat_gas_wb.save(nat_gas_file_path)
    nat_gas_wb.close()

    print("Pipeline complete: Downstream Dashboard ChartSheet compiled and added successfully.")