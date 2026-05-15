import requests

url = "http://127.0.0.1:8000/api/upload/"

files = {
    "file": open("datasets/curriculum_cleaned.csv", "rb")
}

response = requests.post(url, files=files)

print("STATUS CODE:", response.status_code)
print("RAW RESPONSE:")
print(response.text)