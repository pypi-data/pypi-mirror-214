import os

import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def set_cell_width(num):
    if num == 1 or num == 2:
        return 50
    else:
        return 30


def generate(invoices_path, pdfs_path, image_path, product_id, product_name, amount_purchased, price_per_unit, total_price):
    """
    This function converts Excel files into pdfs
    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")
    for filepath in filepaths:
        pdf = FPDF(orientation='P', unit="mm", format="A4")
        pdf.add_page()

        filename = Path(filepath).stem
        invoice_no, date = filename.split("-")

        pdf.set_font(family="Times", size=16, style='B')
        pdf.cell(w=50, h=8, txt=f"Invoice no. {invoice_no}", ln=1)

        pdf.set_font(family="Times", size=16, style='B')
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")
        columns = list(df.columns)
        columns = [item.replace("_", " ").title() for item in columns]

        pdf.set_font(family="Times", size=12, style='B')
        pdf.set_text_color(100, 100, 100)

        # Add Header
        for i in range(0, len(columns) - 1):
            width = set_cell_width(i)
            pdf.cell(w=width, h=8, txt=columns[i], border=1)

        pdf.cell(w=30, h=8, txt=columns[len(columns) - 1], border=1, ln=1)

        # Add Rows
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=50, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=50, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        # Get Total Price
        total_sum = df["total_price"].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(200, 80, 80)

        for i in range(0, len(columns) - 1):
            width = set_cell_width(i)
            pdf.cell(w=width, h=8, txt="", border=1)

        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)
        pdf.set_font(family="Times", size=12)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=f"The total price is CAD ${float(total_sum)}", ln=1)
        pdf.set_font(family="Times", size=14, style='B')
        pdf.cell(w=25, h=8, txt=f"PythonHow ")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)

        pdf.output(f"{pdfs_path}/{filename}.pdf")


