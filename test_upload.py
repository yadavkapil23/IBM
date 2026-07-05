import requests

def test_upload():
    url = "http://localhost:8000/api/v1/upload/"
    
    # Create a dummy file in memory
    files = [
        ('files', ('test_document.pdf', b'dummy content', 'application/pdf')),
        ('files', ('test_spreadsheet.xlsx', b'dummy content xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
    ]
    
    response = requests.post(url, files=files)
    
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    test_upload()
