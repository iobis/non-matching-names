import requests
import csv

res = requests.get("https://api.obis.org/checklist/nomatch").json()["results"]

names = [{
  "scientificName": name["scientificName"],
  "records": name["records"],
  "scientificNameID": "|".join([id["scientificNameID"] for id in name["scientificNameID"]])
} for name in res]

csv_cols = ["scientificName", "records", "scientificNameID"]

with open("list.csv", "w") as csv_file:
  writer = csv.DictWriter(csv_file, fieldnames=csv_cols)
  writer.writeheader()
  
  for row in names:
    writer.writerow(row)
