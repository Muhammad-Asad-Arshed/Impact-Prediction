# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:32:32 2019

@author: Maharvi
"""
from selenium import webdriver
import datetime
import pandas as pd
#set start date 
sdt=datetime.datetime(2007,12,31)
#end date
edt=datetime.datetime(2019,1,1)
#file setting
df = pd.DataFrame(columns=['Date','Rate'])
#from to conversion
fr=input("Enter From Rate Type=")
to=input("Enter To Rate Type=")
ch='4'
while(ch=='4'):
 print("Select\n1:Intlernational Forex Rates\n2:Pakistan Open Market Rates\n3:Pakistan Inter Bank Rates")
 ch=input("Enter Your Choice=")
 if(ch=='1'):
  t='Intlernational Forex Rates'
 elif(ch=='2'):
  t='Pakistan Open Market Rates'
 elif(ch=='3'):
  t='Pakistan Inter Bank Rates'
 else:
  print('Please Enter Value 1 or 2 or 3')
  ch='4' 
op = webdriver.ChromeOptions()
op.add_argument('headless')
# Using Chrome to access web
driver = webdriver.Chrome(options=op)
# Open the website
driver.get('http://www.forex.pk/currency-converter.php')
while(sdt<=edt):
 m=sdt.strftime("%b")
 d=sdt.strftime("%d")
 if(d[0]=='0'):
   d=d[1]
 y=sdt.strftime("%Y")
# Select the day box
 day_box = driver.find_element_by_id('day')
# Send id information
 day_box.send_keys(d)
# Select the Month box
 month_box = driver.find_element_by_id('month')
# Send id information
 month_box.send_keys(m)
# Select the year box
 year_box = driver.find_element_by_id('year')
# Send id information
 year_box.send_keys(y)

# Select the type box
 type_box = driver.find_element_by_id('type')
# Send id information
 type_box.send_keys(t)
# Select the amount box
 amount_box = driver.find_element_by_id('Amount')
# Send id information
 amount_box.send_keys('')
# Select the from box
 curi_box = driver.find_element_by_id('currid1_ajax')
# Send id information
 curi_box.send_keys(fr)
# Select the to box
 curi_box = driver.find_element_by_id('currid2_ajax')
# Send id information
 curi_box.send_keys(to)
# select button 
 butn = driver.find_element_by_id('SubmitCalc')
# click
 butn.click()
 content = driver.find_element_by_class_name('box')
 l=str(content.text)
 m=l.splitlines()
 s=str(m[1])
 s=s[17:]
 print(s)
 df = df.append({'Date': sdt.strftime('%A %d %B %Y'),'Rate':s}, ignore_index=True)
# Create a Pandas Excel writer using XlsxWriter as the engine.
 writer = pd.ExcelWriter('Rates.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
 df.to_excel(writer, sheet_name='Sheet1')
# Get the xlsxwriter workbook and worksheet objects.
 workbook  = writer.book
 worksheet = writer.sheets['Sheet1']
# Add some cell formats
 format1= workbook.add_format()
 format2 = workbook.add_format({'num_format':'0.0000'})
 worksheet.set_column('B:B', 50, format1)
 worksheet.set_column('C:C', 20, format2)
 sdt=sdt+datetime.timedelta(days=1)
 driver.back()
writer.close()
