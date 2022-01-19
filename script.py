import requests
import csv
import pandas as pa
import math

names = requests.get("https://api.obis.org/checklist/nomatchvliz").json()["results"]

vliz_list = pa.read_excel("vliz_list/Blacklist_update_20200626.xlsx", engine="openpyxl", na_values=["NA"], converters={"annotation_type": str, "annotation_resolved_AphiaID": str})
vliz_list.set_index("scientificname_original", inplace=True)

for i in range(len(names)):
    name = names[i]["scientificname"]
    if name in vliz_list.index:
        entries = vliz_list.loc[[name]]
        if len(entries) == 1:
            names[i]["annotation_type"] = entries["annotation_type"][0]
            if isinstance(entries["annotation_resolved_AphiaID"][0], str) or not math.isnan(entries["annotation_resolved_AphiaID"][0]):
                names[i]["annotation_aphiaid"] = entries["annotation_resolved_AphiaID"][0]

csv_cols = ["scientificname", "scientificnameid", "records", "phylum", "class", "order", "family", "genus", "annotation_type", "annotation_aphiaid", "datasets"]

with open("list_annotated.csv", "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_cols)
    writer.writeheader()

    for row in names:
        if "annotation_type" in row:
            writer.writerow(row)

with open("list_open.csv", "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_cols)
    writer.writeheader()

    for row in names:
        if "annotation_type" not in row:
            writer.writerow(row)