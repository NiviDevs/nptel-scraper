import requests

r = requests.get("https://nptel.ac.in/courses")
print(r.status_code)
print(r.text[:500])

with open(
    "downloadable_html.html",
    "w",
) as f:
    f.write(r.text)
# raw html i shal not push because its like 30k lines dawg
