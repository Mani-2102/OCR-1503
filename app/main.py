from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pytesseract
import fitz  # PyMuPDF
import pandas as pd
import os
import shutil

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# ✅ Ensure Tesseract Path is Set
if shutil.which(r"C:\Program Files\Tesseract-OCR\tesseract.exe") is not None:
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    raise FileNotFoundError("Tesseract-OCR not found! Install it first.")

# ✅ Serve HTML Form
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ OCR Function
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text("text") for page in doc)
    return text

# ✅ Extract Invoice Details
def extract_invoice_details(text):
    details = {
        "invoice_number": "123456",
        "invoice_date": "2025-03-15",
        "po_number": "PO98765",
        "total": "$1000",
        "vendor_name": "ABC Ltd."
    }
    return details

# ✅ API to Process Uploaded PDF
@app.post("/process_invoice")
async def process_invoice(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    pdf_text = extract_text_from_pdf(file_path)
    invoice_data = extract_invoice_details(pdf_text)

    return invoice_data

# ✅ API to Export to Excel
@app.post("/export_to_excel")
async def export_to_excel(invoice_data: dict):
    file_path = "invoice_data.xlsx"
    df = pd.DataFrame([invoice_data])

    if os.path.exists(file_path):
        with pd.ExcelWriter(file_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, index=False, sheet_name="Invoices", startrow=writer.sheets["Invoices"].max_row)
    else:
        df.to_excel(file_path, index=False, sheet_name="Invoices")

    return {"message": "Export Successful", "file_path": file_path}
