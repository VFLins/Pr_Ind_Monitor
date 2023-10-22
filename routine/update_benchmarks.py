from bs4 import BeautifulSoup
from pyreadr import read_r
from selenium import webdriver
from selenium.webdriver.common.by import By
from os import getcwd, path
import pandas as pd
import requests
import re

DRIVER = webdriver.Chrome()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57"

#### Update avg fps data from Tom's Hardware ####
#################################################
def get_th_avg_fps() :
    response = requests.get(
        "https://www.tomshardware.com/reviews/gpu-hierarchy,4388.html",
        headers={"User-Agent" : UA})
        
    webpage = BeautifulSoup(DRIVER.page_source, "lxml")
    webpage_tables = webpage.find_all("table")
    
    def build_table(body_obj):
        row_objs = body_obj.find_all("tr")
        rows = list()
        
        for obj in row_objs:
            rowitem_objs = obj.find_all("td")
            row_data = [i.get_text() for i in rowitem_objs]
            rows.append(row_data)
        return rows
    
    def get_fps_val(string):
        re_match = re.search("\d+\.\d(?=[fps])", string)
        return float(re_match.group(0)) if re_match else None
    
    tbl_titles = ["raster", "rt"]
    tbl_header = [
        "model", "fhd_ultra", "fhd_medium", "qhd_ultra", "uhd_ultra", "specs"]
        
    for table, title in zip(webpage_tables, tbl_titles):
        tbl_body = table.find("tbody")
        body = build_table(tbl_body)
        
        df = pd.DataFrame(body, columns=tbl_header)
        for colname in tbl_header[1:5]:
            df[colname] = df[colname].apply(get_fps_val)
        
        df.to_csv(f"data/tomshardware_{title}_avg_fps.csv", index=False)


#### Update V-Ray 5 render benchmark data from official page ####
#################################################################

URL = "https://benchmark.chaos.com/v5/vray-gpu-cuda"

MODEL_NAMES = read_r(getcwd() + "\data\prices.rds")[None]["ProductName"]\
    .unique()

def get_vray5_render_pts():
    DRIVER = webdriver.Chrome()
    DRIVER.get(URL)
    
    results = []
    for model in MODEL_NAMES:
        #params = {
        #    "gpu" : f"{model};1",
        #    "show-hybrid" : "false",
        #    "my-scores-only" : "false"
        #}
        
        #response_url = requests.get(URL, params=params).url
        #print(response_url)
        
        
        navigate = DRIVER.find_element(By.CLASS_NAME, "advanced")
        navigate.click()
        
        d_name_box = "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/ul/li/ol/li/span[1]/div/input"
        d_count_box = "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/ul/li/ol/li/span[2]/div/input"
        
        DRIVER.find_element(By.XPATH, d_name_box).clear()
        DRIVER.find_element(By.XPATH, d_name_box).send_keys(model)
        
        DRIVER.find_element(By.XPATH, d_count_box).clear()
        DRIVER.find_element(By.XPATH, d_count_box).send_keys("1")
        
        search_btn = "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div/button"
        navigate = DRIVER.find_element(By.XPATH, search_btn)
        navigate.click()
        
        webpage = BeautifulSoup(DRIVER.page_source, "lxml")
        webpage.find("localised-number").get_text()
        
    DRIVER.quit()
    
# run from command line 'python3 ./routine/update_benchmarks.py'
if __name__ == "__main__":
    try: get_th_avg_fps()
    except Exception as expt: 
        print("Error trying to collect Avg. FPS from Tom's Hardware")
        print(expt)
    
    #if path.isfile(getcwd() + "\data\prices.rds"):
    #    try: get_vray5_render_pts()
    #    except Exception as expt: 
    #    print("Error trying to collect performance from Vray-5 Benchmarks")
    #    print(expt)
    #else: 
    #    print("Not able to collect Vray-5 benchmarks, '\data\prices.rds' not found in this folder")
    
    
