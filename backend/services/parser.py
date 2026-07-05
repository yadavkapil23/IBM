def process_document(filename: str, content: bytes) -> dict:
    """
    Stub for document processing.
    In later phases, this will use PyMuPDF, tesseract, etc. based on file extension.
    """
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    text = ""
    
    if ext == "pdf":
        text = f"Simulated parsed text from PDF: {filename}"
    elif ext in ["docx", "doc"]:
        text = f"Simulated parsed text from Word Document: {filename}"
    elif ext in ["xlsx", "xls"]:
        text = f"Simulated parsed text from Excel Spreadsheet: {filename}"
    else:
        text = f"Unsupported or unknown file type: {filename}"
        
    return {
        "metadata": {
            "extension": ext,
            "size_bytes": len(content)
        },
        "text": text
    }
