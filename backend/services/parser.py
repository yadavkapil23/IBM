import io
import fitz # PyMuPDF
import docx
import pandas as pd

def process_document(filename: str, content: bytes) -> dict:
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    text = ""
    
    try:
        if ext == "pdf":
            # PyMuPDF can open from bytes by specifying the filetype
            doc = fitz.open("pdf", content)
            for page in doc:
                text += page.get_text()
            doc.close()
        elif ext in ["docx", "doc"]:
            doc = docx.Document(io.BytesIO(content))
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif ext in ["xlsx", "xls"]:
            # pandas can read excel from a BytesIO object
            df = pd.read_excel(io.BytesIO(content))
            text = df.to_csv(index=False)
        else:
            text = f"Unsupported or unknown file type: {filename}"
    except Exception as e:
        text = f"Error processing {filename}: {str(e)}"
        
    return {
        "metadata": {
            "extension": ext,
            "size_bytes": len(content)
        },
        "text": text
    }
