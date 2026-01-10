import requests

r = requests.get("https://nptel.ac.in/courses")
print(r.status_code)
print(r.text[:500])
