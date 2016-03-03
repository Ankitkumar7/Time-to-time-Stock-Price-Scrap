# Stock Data Module created on 20-01-2015                                #
# We use Schedule, Tabulate,Date and Time ,BeautifulSoup, sqlite3 Module #
# Scraping Stock price from Yahoo finance Website,                       #
# Every 1 minute the price will update and it will export to database    #
#                                                                        #
#************************************************************************#
#Module Schedule
import sched, time
#Module Tabulate
from tabulate import tabulate
#Module BeautifulSoup
import requests
from bs4 import BeautifulSoup
#Data and Time Module
from time import gmtime,strftime
import sqlite3
conn = sqlite3.connect('stocks.db')
conn.execute('''CREATE TABLE IF NOT EXISTS Stock_Market (StockName TEXT , StockPrice TEXT,datetime TEXT,TimeStamp TEXT);''')
#scheduler declaration
s = sched.scheduler(time.time,time.sleep)#time.time running time,#time.sleep sleeping time
#System Time
Current_Time = strftime("%Y-%m-%d %H:%M:%S",gmtime())

## Open the file with read only permit
f = open('symbol.txt', "r")

## use readlines to read all lines in the file
## The variable "lines" is a list containing all lines
lines = f.readlines()

## close the file after reading the lines.
f.close()
#Standard Variable
span_id = "yfs_l84_%s"

url = "https://in.finance.yahoo.com/q?s=%s"

#Defining Function for data update
def Stock_Data_Update():
    for i in range(len(lines)):
        st1 = url%lines[i].lower()
        r =  requests.get(st1)
        soup = BeautifulSoup(r.content)
        get1 = soup.find_all("span", {"id":span_id%lines[i].lower().rstrip()})
    
        for item in get1:
            print item.text,lines[i]
            conn.execute("insert into Stock_Market (StockName, StockPrice, datetime,TimeStamp) values (?, ?, ?,?)",(lines[i], item.text, Current_Time,time.time()))
            conn.commit()
            
    
   

#Defining function for schedule
def Run_Time():
    for i in range(360):
        s.enter(1,1,Stock_Data_Update,())
        s.run()

print Run_Time()
