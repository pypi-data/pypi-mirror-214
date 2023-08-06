import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path
import os

# import path

def generate(files_path='excel', pdf_path='pdfs', image='pythonhow.png', total_column='total_price'):
    """_summary_
    This function converts invoice excel with 5 columns files to pdfs invoices. 
    Args:
        files_path (str, optional): _description_. Defaults to 'excel'.
        pdf_path (str, optional): _description_. Defaults to 'pdfs'.
        image (str, optional): _description_. Defaults to 'pythonhow.png'.
    """

    filepaths = glob.glob(f"{files_path}/*.xlsx")

    for filepath in filepaths:

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        filename = Path(filepath).stem
        invoice_nr, date_nr = filename.split("-")
        pdf.add_page()
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=16, h=16, txt=f"Invoice nr: {invoice_nr}", ln=1)
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=16, h=1, txt=f"Date: {date_nr}", ln=1)
        data = pd.read_excel(filepath, sheet_name="Sheet 1")
        columns_a = [x.replace("_", " ").title() for x in list(data.columns)]
        pdf.ln(10)
        pdf.set_font(family="Times", size=12, style="B")
        pdf.cell(w=30, h=12, txt=columns_a[0], border=1)
        pdf.cell(w=50, h=12, txt=columns_a[1], border=1)
        pdf.cell(w=45, h=12, txt=columns_a[2], border=1)
        pdf.cell(w=40, h=12, txt=columns_a[3], border=1)
        pdf.cell(w=30, h=12, txt=columns_a[4], border=1, ln=1)
        
        column_name = list(data.columns)
        
        for index, rows in data.iterrows():
            i = 0
            pdf.set_font(family="Times", size=12)
            pdf.cell(w=30, h=10, txt=str(rows[column_name[i]]), border=1)
            i= i+1
            pdf.cell(w=50, h=10, txt=str(rows[column_name[i]]), border=1)
            i= i+1
            pdf.cell(w=45, h=10, txt=str(rows[column_name[i]]), border=1)
            i= i+1
            pdf.cell(w=40, h=10, txt=str(rows[column_name[i]]), border=1)
            i= i+1
            pdf.cell(w=30, h=10, txt=str(rows[column_name[i]]), border=1, ln=1)

        total = data[total_column].sum()
        pdf.set_font(family="Times", size=12)
        pdf.cell(w=30, h=10, txt="", border=1)
        pdf.cell(w=50, h=10, txt="", border=1)
        pdf.cell(w=45, h=10, txt="", border=1)
        pdf.cell(w=40, h=10, txt="", border=1)
        pdf.cell(w=30, h=10, txt=str(total), border=1, ln=1)
        pdf.ln(5)
        pdf.set_font(family="Times", size=12, style="B")
        pdf.cell(w=30, h=10, txt=f"The total price is {total}", ln=1)
        pdf.ln(2)
        pdf.set_font(family="Times", size=12, style="B")
        pdf.cell(w=22, h=10, txt="Pythonhow")
        pdf.image(f"{image}", w=10)
        if not os.path.exists(pdf_path):
            os.mkdir(pdf_path)
        pdf.output(f"{pdf_path}/{filename}.pdf")

    # print(data)

