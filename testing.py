#!/usr/bin/env python
# coding: utf-8

# In[105]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import requests
import json

import datetime
import re
from dateutil.relativedelta import relativedelta



# In[2]:


#! pip install streamlit


# In[3]:


import streamlit as st


# In[4]:


import time
import string
import pandas as pd
from selenium.webdriver.common.keys import Keys
import html_to_json
dict_way_bill_dates = dict()
wait_time_sec = 10 
df = pd.DataFrame()

def driver_load():
    return webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        
def test_cargo(code_dict):
    for way_bill in code_dict:
        # load driver
        driver = driver_load()
        searchAddress = "https://www.cma-cgm.com/ebusiness/tracking"
        try:
            driver.get(searchAddress)
            time.sleep(wait_time_sec)
            # enter way_bill number in input field
            element = driver.find_element(By.XPATH,"//*[@id='Reference']")
            element.send_keys(way_bill)
            # click submit button
            submit = driver.find_element(By.XPATH,"//*[@id='btnTracking']")
            submit.click()
            time.sleep(2)
            # get ETA
            x = driver.find_element(By.XPATH,'//*[@id="gridTrackingDetails"]/div[2]/table//tr[last()]//td[last()-4]').text
            y = driver.find_element(By.XPATH,'//*[@id="gridTrackingDetails"]/div[2]/table//tr[last()]//td[last()-2]').text
            # location is given as Eg. MONTREAL, QC. Pick only montreal
            location = y.split(",")[0]
            # Example of date format "Friday, 13-May-202206:00" received
            reformat_x = re.findall("\d\d?-[a-zA-Z]{3}-[0-9]{4}",x)[0]
            x_new = pd.to_datetime(reformat_x,format="%d-%b-%Y").strftime("%Y-%m-%d")
            df.loc[way_bill,"location"] = location
            df.loc[way_bill,"ETA"] = x_new
            dict_way_bill_dates[way_bill] = [x_new]
            driver.close()
            
        except:
            dict_way_bill_dates[way_bill] = ""
            df.loc[way_bill,"ETA"] = ""
            location = ""
            df.loc[way_bill,"location"] = location
            driver.close()
    return df


# In[ ]:


#uploaded_file = st.file_uploader('Choose a file')
#df1=pd.read_csv(uploaded_file)


# In[ ]:


df1 = test_cargo(["SEKU9064057","CGMU6925021"])
df1

