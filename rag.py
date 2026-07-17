import requests
import json

def test_rag_pipeline():
    base_url = "http://localhost:8000/api/v1"
    
    files = [
        ('files', ('', b'The company revenue for the fiscal year 2023 was $50 Million. Total debt stands at $10 Million, with positive cash flow.', 'text/plain'))
    ]
    upload_res = requests.post(f"{base_url}/upload/", files=files)
    print("Upload Status:", upload_res.status_code)
    print("Upload Response:", json.dumps(upload_res.json(), indent=2))
    
    query_payload = {
        "top_k": 2
    }
    query_res = requests.post(f"{base_url}/query/", json=query_payload)
    print("Query Status:", query_res.status_code)
    print("Query Response:", json.dumps(query_res.json(), indent=2))

if __name__ == "__main__":
    test_rag_pipeline()
