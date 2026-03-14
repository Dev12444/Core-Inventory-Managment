import requests
import json

url = 'http://127.0.0.1:5000/operations/receipt/create'
data = {
    'vendor_id': 1,
    'warehouse_id': 1,
    'items': [
        {'product_id': 1, 'qty': 50},
        {'product_id': 2, 'qty': 20}
    ]
}

try:
    response = requests.post(url, json=data, timeout=5)
    print('Status:', response.status_code)
    print('Response:', response.json())
except Exception as e:
    print('Error:', e)