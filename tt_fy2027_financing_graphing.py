import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.series_factory import SeriesFactory
from openpyxl.chart.axis import ChartLines
from pathlib import Path

file_path = Path.cwd().joinpath("TT_Central_Gov_2026_Financing.xlsx")
wb = openpyxl.load_workbook(file_path)

ws = wb.active

borrow_chart = BarChart()
borrow_chart.x_axis.delete = False
borrow_chart.y_axis.delete = False
borrow_chart.type = "col"
borrow_chart.style = 12
borrow_chart.grouping = "stacked"
borrow_chart.overlap = 100

borrow_chart.title = "Central Government Gross Financing Architecture (TT$ Millions)"
borrow_chart.x_axis.title = "Financial Year Period"
borrow_chart.y_axis.title = "Amount (TT$ Millions)"
borrow_chart.y_axis.tickLblPos = "nextTo"
borrow_chart.y_axis.number_format = '$#,###.0'
borrow_chart.y_axis.majorGridlines = ChartLines()

if ws is not None:
    # HSF transfer data processing
    borrow_chart_hsf_data_ref = Reference(ws, min_col=1, max_col= 7, min_row=5, max_row= 5)
    borrow_chart_hsf_cat_ref = Reference(ws, min_col= 2, max_col= 7, min_row= 1, max_row= 1)
    

    # Domestic borrowing data processing
    borrow_chart_domestic_data_ref = Reference(ws, min_col=1, max_col= 7, min_row=9, max_row= 9)
    borrow_chart_domestic_cat_ref = Reference(ws, min_col= 2, max_col= 7, min_row= 1, max_row= 1)

    # External borrowing data processing
    borrow_chart_ext_data_ref = Reference(ws, min_col=1, max_col= 7, min_row=4, max_row= 4)
    borrow_chart_ext_cat_ref = Reference(ws, min_col= 2, max_col= 7, min_row= 1, max_row= 1)

    # Add colummns to chart
    borrow_chart.add_data(borrow_chart_hsf_data_ref, titles_from_data= True, from_rows= True)
    borrow_chart.add_data(borrow_chart_domestic_data_ref, titles_from_data= True, from_rows= True)
    borrow_chart.add_data(borrow_chart_ext_data_ref, titles_from_data= True, from_rows= True)
    borrow_chart.set_categories(borrow_chart_hsf_cat_ref)

    colors = ["2ECC71", "2980B9", "E67E22"]
    for i, color_hex in enumerate(colors):
        if i < len(borrow_chart.series):
            borrow_chart.series[i].graphicalProperties.solidFill = color_hex
            borrow_chart.series[i].graphicalProperties.line.solidFill = color_hex

    borrow_chart_sheet = wb.create_chartsheet(title="TT_Gov_Borrowing")
    borrow_chart_sheet.add_chart(borrow_chart)
    wb.save(file_path)

    print("Pipeline complete. TT Government Borrowing Charts created")
    wb.close()