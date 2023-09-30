from bs4 import BeautifulSoup
import pandas as pd
import requests

response = requests.get(
    "https://www.tomshardware.com/reviews/gpu-hierarchy,4388.html",
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"})
    
webpage = BeautifulSoup(response.text, "lxml")
webpage_tables = webpage.find_all("table")

#def build_header(header_obj):
#    header_items = header_obj.find_all("th")
#    return [i.get_text() for i in header_items]

def build_table(body_obj):
    row_objs = body_obj.find_all("tr")
    rows = list()
    
    for obj in row_objs:
        rowitem_objs = obj.find_all("td")
        row_data = [i.get_text() for i in rowitem_objs]
        rows.append(row_data)
    return rows


tbl_titles = ["raster", "rt"]
tbl_header = [
    "Model", "1080p_Ultra", "1080p_Medium", "1440p_Ultra", "4K_Ultra", "Specs"]
    
for table, title in zip(webpage_tables, tbl_titles):
    #tbl_header = build_header(tbl_header)
    tbl_body = table.find("tbody")
    body = build_table(tbl_body)
    pd.DataFrame(body, columns=tbl_header).to_csv(f"data/{title}_avg_fps.csv")

