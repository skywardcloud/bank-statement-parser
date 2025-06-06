from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import shutil
import os
from parser import parse_csv, validate_balance

app = FastAPI()

# Enable CORS so frontend can access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "../data"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Accepts a CSV file and saves it to the data directory
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully."
    }

@app.post("/parse")
async def parse_and_validate(filename: str):
    """
    Parses the uploaded CSV and returns transaction data + validation
    """
    filepath = os.path.join(UPLOAD_DIR, filename)

    # Step 1: Parse CSV
    transactions = parse_csv(filepath)

    # Step 2: Validate balances
    validation = validate_balance(transactions)

    return {
        "transactions": transactions,
        "validation": validation
    }
