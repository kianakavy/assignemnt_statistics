# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 20:26:44 2023

@author: kiana
"""

import pandas as pd
import os
import pyodbc
import numpy as np
import seaborn as sns
import geopandas as gpd
from patsy import dmatrices
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from stargazer.stargazer import Stargazer
from IPython.core.display import HTML
from linearmodels.panel import PanelOLS
from tabulate import tabulate

os.chdir('C:\\Users\\kiana\\OneDrive\\Dokumente\\Bachelor Literatur')
os.getcwd() 

# set up some constants
MDB = 'C:/Users/kiana/OneDrive/Dokumente/Bachelor Literatur/SRC2004.accdb'
DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'

# connect to db
con = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB))
cur = con.cursor()

# run a query and get the results 
SQL = 'SELECT * FROM [MISCELLANEOUS_SCHOOL];'

rows = cur.execute(SQL).fetchall()

# get column names from cursor description
columns = [column[0] for column in cur.description]

# create a pandas dataframe
df = pd.DataFrame.from_records(rows, columns=columns)

# close cursor and connection
cur.close()
con.close()

# print dataframe
print(df.head())

df=df.loc[:,["BEDS_CD", "YEAR", "SCHOOL_NAME","DISTRICT_NAME"] ]



district_values = [
    f"New York City Geographic District # {i}" for i in range(1, 10)
    ] + [
    f"New York City Geographic District #{i}" for i in range(10, 33)
] #because 06 only has geo we need to use that

df = df[df['DISTRICT_NAME'].isin(district_values)]

     
###loading regents now#########################################################
cons = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB))
curs = cons.cursor()

# run a query and get the results 
SQLs = 'SELECT * FROM [regents];'

rows_ = curs.execute(SQLs).fetchall()

# get column names from cursor description***
columns_ = [column[0] for column in curs.description]

# create a pandas dataframe
regents = pd.DataFrame.from_records(rows_, columns=columns_)


report_card_04=df.merge(regents, on = ['BEDS_CD','YEAR'], how = 'left')

#drop all rows for which 
report_card_04=report_card_04.dropna().reset_index(drop=True)
report_card_04=report_card_04[report_card_04["Tested"]>="5"]
###### we now have new_df with 2004 data## now repeat for rest lol

###############################################################################

MDB_1 = 'C:/Users/kiana/OneDrive/Dokumente/Bachelor Literatur/SRC2005.accdb'

const = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB_1))
curso = const.cursor()

# run a query and get the results 
SQL1 = 'SELECT * FROM [Regents];'

rows_1 = curso.execute(SQL1).fetchall()

# get column names from cursor description
columns_1 = [column[0] for column in curso.description]

# create a pandas dataframe
regents_05 = pd.DataFrame.from_records(rows_1, columns=columns_1)
regents_05=regents_05[regents_05["Tested"]>="5"]

#############################################################same for district
const_2 = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB_1))
curso_2 = const_2.cursor()

# run a query and get the results 
SQL_2 = 'SELECT * FROM [MISCELLANEOUS_SCHOOL];'

rows_2 = curso_2.execute(SQL_2).fetchall()

# get column names from cursor description
columns_2 = [column[0] for column in curso_2.description]

# create a pandas dataframe
district_05 = pd.DataFrame.from_records(rows_2, columns=columns_2)

district_05=district_05.loc[:,["BEDS_CD", "YEAR", "SCHOOL_NAME","DISTRICT_NAME"] ]


district_05 = district_05[district_05['DISTRICT_NAME'].isin(district_values)]


#meeeeerge
report_card_05=district_05.merge(regents_05, on = ['BEDS_CD','YEAR'], how = 'left')
report_card_05=report_card_05.dropna().reset_index(drop=True)

##############################################################################
MDB_2 = 'C:/Users/kiana/OneDrive/Dokumente/Bachelor Literatur/SRC2006.accdb'

const_3 = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB_2))
curso_3 = const_3.cursor()

# run a query and get the results 
SQL_3 = 'SELECT * FROM [Regents Results 2005-06];'

rows_3 = curso_3.execute(SQL_3).fetchall()

# get column names from cursor description
columns_3 = [column[0] for column in curso_3.description]

# create a pandas dataframe
regents_06 = pd.DataFrame.from_records(rows_3, columns=columns_3)
regents_06=regents_06[regents_06["Tested"]>=5]

#############################################################same for district
const_4 = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB_2))
curso_4 = const_4.cursor()

# run a query and get the results 
SQL_4 = 'SELECT * FROM [Miscellaneous School Data];'

rows_4 = curso_4.execute(SQL_4).fetchall()

# get column names from cursor description
columns_4 = [column[0] for column in curso_4.description]

# create a pandas dataframe
district_06 = pd.DataFrame.from_records(rows_4, columns=columns_4)

district_06=district_06.loc[:,["BEDS_CD", "YEAR", "SCHOOL_NAME","DISTRICT_NAME"] ]

district_06_values = [
    f"NYC GEOG DIST {i}" for i in range(1, 33)
    ] 


district_06 = district_06[district_06['DISTRICT_NAME'].isin(district_06_values)]


#meeeeerge
report_card_06=district_06.merge(regents_06, on = ['BEDS_CD','YEAR'], how = 'left')
report_card_06=report_card_06.dropna().reset_index(drop=True)



##############################################################################
MDB_5 = 'C:/Users/kiana/OneDrive/Dokumente/Bachelor Literatur/SRC2007.mdb'

const_5 = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB_5))
curso_5 = const_5.cursor()

# run a query and get the results 
SQL_5 = 'SELECT * FROM [Regents Examination Annual Results];'

rows_5 = curso_5.execute(SQL_5).fetchall()

# get column names from cursor description
columns_5 = [column[0] for column in curso_5.description]

# create a pandas dataframe
regents_07 = pd.DataFrame.from_records(rows_5, columns=columns_5)
regents_07=regents_07[regents_07["TESTED"]>=5]

#############################################################same for district
const_6 = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB_5))
curso_6 = const_6.cursor()

# run a query and get the results 
SQL_6 = 'SELECT * FROM [Staff];'

rows_6 = curso_6.execute(SQL_6).fetchall()

# get column names from cursor description
columns_6 = [column[0] for column in curso_6.description]

# create a pandas dataframe
district_07 = pd.DataFrame.from_records(rows_6, columns=columns_6) 

district_07=district_07.loc[:,["ENTITY_CD", "YEAR", "SCHOOL_NAME","DISTRICT_NAME"] ]

district_07_values = [
    f"NYC GEOG DIST {i}" for i in range(1, 33)
    ]  


district_07 = district_07[district_07['DISTRICT_NAME'].isin(district_07_values)]


#meeeeerge
report_card_07=district_07.merge(regents_07, on = ['ENTITY_CD','YEAR'], how = 'left')
report_card_07=report_card_07.dropna().reset_index(drop=True)

##################################################################################################

# Set up database connection
MDB = 'C:/Users/kiana/OneDrive/Dokumente/Bachelor Literatur/SRC{}.accdb'
DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'
# Define years to fetch data for
years = range(2008, 2017)

# Initialize dictionary to store results for each year
report_cards = {}

# Loop over years
for year in years:
    # Construct database path for current year
    accdb_path = MDB.format(year)

    # Connect to database
    conn = pyodbc.connect('DRIVER={};DBQ={}'.format(DRIVER, accdb_path))
    cursor = conn.cursor()

    # Fetch Regents Examination Annual Results data
    sql = 'SELECT * FROM [Regents Examination Annual Results];'
    rows = cursor.execute(sql).fetchall()
    columns = [column[0] for column in cursor.description]
    regents = pd.DataFrame.from_records(rows, columns=columns)
    regents = regents[regents["TESTED"] >= 5]

    # Fetch district data
    sql = 'SELECT * FROM [Staff];'
    rows = cursor.execute(sql).fetchall()
    columns = [column[0] for column in cursor.description]
    district = pd.DataFrame.from_records(rows, columns=columns)
    district = district.loc[:,["ENTITY_CD", "YEAR", "DISTRICT_NAME"]]
    district_values = [f"NYC GEOG DIST {i}" for i in range(1, 33)] 
    district = district[district['DISTRICT_NAME'].isin(district_values)]

    # Merge data
    report_card = district.merge(regents, on=['ENTITY_CD', 'YEAR'], how='left')
    report_card = report_card.dropna().reset_index(drop=True)

    # Store report card for current year in dictionary
    report_cards[year] = report_card

    # Close database connection
    conn.close()
#accessing report cards
report_card_08 = report_cards[2008]
report_card_09 = report_cards[2009]
report_card_10 = report_cards[2010]
report_card_11 = report_cards[2011]
report_card_12 = report_cards[2012]
report_card_13 = report_cards[2013]
report_card_14 = report_cards[2014]
report_card_15 = report_cards[2015]
report_card_16 = report_cards[2016]
##############################################################################
MDB_17 = 'C:/Users/kiana/OneDrive/Dokumente/Bachelor Literatur/SRC2017.mdb'

const_17 = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB_17))
curso_17= const_17.cursor()

# run a query and get the results 
SQL_17 = 'SELECT * FROM [Regents Examination Annual Results];'

rows_17 = curso_17.execute(SQL_17).fetchall()

# get column names from cursor description
columns_17 = [column[0] for column in curso_17.description]

# create a pandas dataframe
regents_17 = pd.DataFrame.from_records(rows_17, columns=columns_17)
regents_17=regents_17[regents_17["TESTED"]>=5]

#############################################################same for district
const_18 = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB_17))
curso_18 = const_18.cursor()

# run a query and get the results 
SQL_18 = 'SELECT * FROM [Staff];'

rows_18 = curso_18.execute(SQL_18).fetchall()

# get column names from cursor description
columns_18 = [column[0] for column in curso_18.description]

# create a pandas dataframe
district_17 = pd.DataFrame.from_records(rows_18, columns=columns_18) 

district_17=district_17.loc[:,["ENTITY_CD", "YEAR", "DISTRICT_NAME"] ]

district_17_values = [
    f"NYC GEOG DIST {i}" for i in range(1, 33)] 


district_17 = district_17[district_17['DISTRICT_NAME'].isin(district_17_values)]


#meeeeerge
report_card_17=district_17.merge(regents_17, on = ['ENTITY_CD','YEAR'], how = 'left')
report_card_17=report_card_17.dropna().reset_index(drop=True)

##################################################################################################
#leaving 2018 out because there is no district name hence no way to localize each regents exam outcome
#so makes 0 sense to involve into our code


########################cleaning up so I can stack up all report cards###########################################

# define old and new column names
old_cols = ['BEDS_CD', 'SUBJECT_CD']
new_cols = ['ENTITY_CD', 'SUBJECT']

# loop through dataframes and rename columns
for df in [report_card_04, report_card_05, report_card_06]:
    df.rename(columns=dict(zip(old_cols, new_cols)), inplace=True)
    df.drop(['GroupLevel', 'GroupLevelCode'], axis=1, inplace=True)


for year in range(2007, 2018):
    report_card_name = 'report_card_' + str(year)[-2:]
    if report_card_name in locals():
        locals()[report_card_name].drop('ENTITY_NAME', axis=1, inplace=True)


for year in range(2004, 2008):
    report_card_name = 'report_card_' + str(year)[-2:]
    if report_card_name in locals():
        locals()[report_card_name].drop('SCHOOL_NAME', axis=1, inplace=True)
        locals()[report_card_name].rename(columns={'Tested':'TESTED'}, inplace=True)


report_card_06.rename(columns={'GROUP_NAME':'SUBGROUP_NAME'}, inplace=True)

report_card_04.insert(4, "SUBGROUP_NAME", "")
report_card_05.insert(4, "SUBGROUP_NAME", "")



for year in range(2006, 2018):
    # get the name of the report card dataframe for the current year
    report_card_name = 'report_card_' + str(year)[-2:]
    # check if the report card dataframe exists
    if report_card_name in locals():
        # define the dictionary of values to replace
        d = {'All Students': ''}
        # replace the values in the 'alphabet' column of the report card dataframe
        locals()[report_card_name]['SUBGROUP_NAME'] = locals()[report_card_name]['SUBGROUP_NAME'].replace(d, regex=True)
        # print the modified report card dataframe to confirm the changes
        print(locals()[report_card_name])


for year in range(2004, 2007):
    report_card_name = 'report_card_' + str(year)[-2:]
    if report_card_name in locals():
        report_card = locals()[report_card_name]
        # convert columns to numeric type
        for c in ['TESTED', '55-100', '65-100', '85-100']:
            report_card[c] = pd.to_numeric(report_card[c], errors='coerce')
            #maybe not coerce find data with nans

        # add the new columns
        report_card["NUM_0-54"] = report_card["TESTED"] - report_card["55-100"]
        report_card["NUM_55-64"] = report_card["55-100"] - report_card["65-100"]
        report_card["NUM_65-84"] = report_card["65-100"] - report_card["85-100"]
        # assign the modified dataframe back to the original variable
        locals()[report_card_name] = report_card

for year in range(2004, 2007):
    report_card_name = 'report_card_' + str(year)[-2:]
    if report_card_name in locals():
        locals()[report_card_name].drop(['55-100', '65-100', '%tested55-100', '%tested65-100'], axis=1, inplace=True)
        
        
for year in range(2004, 2007):
    report_card_name = 'report_card_' + str(year)[-2:]
    locals()[report_card_name].rename(
        columns={
            '85-100':'NUM_85-100','%tested85-100':'PER_85-100'
            }
        , inplace=True
        )


for year in range(2004, 2007):
    report_card_name = 'report_card_' + str(year)[-2:]
    if report_card_name in locals():
        report_card = locals()[report_card_name]
        # convert columns to numeric type
        for c in ['TESTED', 'NUM_0-54', 'NUM_55-64', 'NUM_65-84']:
            report_card[c] = pd.to_numeric(report_card[c], errors='coerce')
            #maybe not coerce find data with nans

        # add the new columns
        report_card["PER_0-54"] = round((report_card["NUM_0-54"]/report_card["TESTED"])*100,0)
        report_card["PER_55-64"] =round((report_card["NUM_55-64"]/report_card["TESTED"])*100,0)
        report_card["PER_65-84"] =round((report_card["NUM_65-84"]/report_card["TESTED"])*100,0)
        # assign the modified dataframe back to the original variable
        locals()[report_card_name] = report_card

for year in range(2004, 2007):
    # get the name of the report card dataframe for the current year
    report_card_name = 'report_card_' + str(year)[-2:]
    # check if the report card dataframe exists
    if report_card_name in locals():
        # define the dictionary of values to replace
        d = {'%': ''}
        # replace the values in the 'alphabet' column of the report card dataframe
        locals()[report_card_name]['PER_85-100'] = locals()[report_card_name]['PER_85-100'].replace(d, regex=True)
        # print the modified report card dataframe to confirm the changes
        print(locals()[report_card_name])
        
        
#re-arrange order of num and pct correctly like for 2007 onwards data
for year in range(2004, 2007):
    # get the name of the report card dataframe for the current year
    report_card_name = 'report_card_' + str(year)[-2:]
    # check if the report card dataframe exists
    if report_card_name in locals():
        # replace the values in the 'alphabet' column of the report card dataframe
        locals()[report_card_name] = locals()[report_card_name].iloc[:,[0,1,2,3,4,5,8,11,9,12,10,13,6,7]]

# loop through the years 2004 and 2005
for year in range(2004, 2006):
    # get the name of the report card dataframe for the current year
    report_card_name = 'report_card_' + str(year)[-2:]
    # check if the report card dataframe exists
    if report_card_name in locals():
        # define the dictionary outside the loop
        d = {
            f'New York City Geographic District # {i}': f'NYC GEOG DIST {i}' 
            for i in range(1, 10)
            }
        e= {
            f'New York City Geographic District #{i}': f'NYC GEOG DIST {i}' 
            for i in range(10,33)
            }
        #important: i put the for loop in here so I don't need to define 31 keys with 
        #according values manually but let spyder do it for me
        # replace the values in the 'DISTRICT_NAME' column of the report card dataframe
        locals()[report_card_name]['DISTRICT_NAME'] = locals()[report_card_name]['DISTRICT_NAME'].replace(d, regex=True)
        locals()[report_card_name]['DISTRICT_NAME'] = locals()[report_card_name]['DISTRICT_NAME'].replace(e, regex=True)
#sth happened here where I haz to correct for reportcard06 bitchez
report_card_06.dropna(inplace=True)
report_card_06["PER_85-100"]=round( pd.to_numeric(report_card_06["PER_85-100"]))


all_report_cards = {}

for year in range(2004, 2018):
    report_card_name = 'report_card_' + str(year)[-2:]
    if report_card_name in locals():
        all_report_cards[report_card_name] = locals()[report_card_name]

all_reports = ()
for year in range(2004,2018):
    report_card_name = 'report_card_' + str(year)[-2:]
    if report_card_name in locals():
        all_reports += (locals()[report_card_name],)
        
all_reports = pd.concat(all_reports, ignore_index=True)
all_reports = all_reports[all_reports["NUM_0-54"] != "s"]

print(all_reports.isnull().values.any())
#false aka no need to get rid of nan values weyoooooo
all_reports.to_csv('all_reports.csv',index=False)
#have created now csv file uh yeah better to work with that now!

##################################################################################

#can now just import csv of "all_reports"

all_reports=pd.read_csv("all_reports.csv",index_col=False)
##############################################################################
# This is for the Stop and Frisk data
##############################################################################
cols = [
        "year", "datestop","pct", "inout", "crimsusp", "explnstp", 
        "arstmade", "frisked", "searched", "sex", "race", "age"
        ]

old_col=["YEAR2", "MONTH2", "LOCATION_IN_OUT_CODE", "SUSPECTED_CRIME_DESCRIPTION",
         "SUSPECT_ARRESTED_FLAG",
         "OFFICER_EXPLAINED_STOP_FLAG", 
         "FRISKED_FLAG", "SEARCHED_FLAG","SUSPECT_REPORTED_AGE", "SUSPECT_SEX",
         "SUSPECT_RACE_DESCRIPTION","STOP_LOCATION_PRECINCT" ]

sqf = {}
for year in range(2004, 2016):
    sqf_name = str(year) + ".csv"
    sqf[year] = pd.read_csv(sqf_name, usecols=cols,index_col=False,
                            encoding='windows-1252' )
    sqf[year] = sqf[year].applymap(
                lambda x: x.strip() if isinstance(x, str) else x)
    sqf[year]['pct']=pd.to_numeric(sqf[year]['pct'])
    sqf[year]=sqf[year][sqf[year]['pct'] != 999]
    sqf[year].dropna(inplace=True)
    
    
 
sqf_16= pd.read_csv("2016.csv", encoding='windows-1252' )
sqf_16.rename(columns={'ï»¿year':'year'}, inplace=True)
sqf_16= sqf_16[cols]
sqf_16['pct']=sqf_16['pct'].replace(' ', np.NaN)
sqf_16.dropna(inplace=True)
sqf_16['pct']=pd.to_numeric(sqf_16['pct'])

sqf_17 = pd.read_excel("2017.xlsx", usecols=old_col)

#change column names of 2017 data 

new_col=[
    "year","month","inout", "crimsusp","arstmade", "explnstp", 
         "frisked", "searched", "age","sex", "race", "pct"
        ]
sqf_17.rename(columns=dict(zip(old_col, new_col)), inplace=True)





def extract_month(date_int):
    date_str = str(date_int)
    if len(date_str) == 8:
        return date_str[0:2]
    elif len(date_str) == 7:
        return date_str[0]
    else:
        return None
 
def new_year_06(date_int):
    date_str = str(date_int)
    year_str = date_str[0:4]
    if year_str=="2006":
        return year_str
    else: 
        return np.nan
    
def extract_month_06(date_int):
    date_str = str(date_int)
    month_str = date_str[5:7]
    if month_str.startswith('0'):
        return month_str[1] 
    else:
        return month_str 
    
for year in range(2004,2006):
    sqf[year]["month"] = sqf[year]["datestop"].apply(extract_month)


for year in range(2007,2016):
    sqf[year]["month"] = sqf[year]["datestop"].apply(extract_month)


sqf_16['month'] = sqf_16["datestop"].apply(extract_month)

sqf[2006]["month"] = sqf[2006]["datestop"].apply(extract_month_06)

sqf[2006]["year"] = sqf[2006]["datestop"].apply(new_year_06)
sqf[2006].dropna(inplace=True)



#change column names of 2017 data 
old_col=["YEAR2", "MONTH2", "LOCATION_IN_OUT_CODE", "SUSPECTED_CRIME_DESCRIPTION",
         "SUSPECT_ARRESTED_FLAG",
         "OFFICER_EXPLAINED_STOP_FLAG", 
         "FRISKED_FLAG", "SEARCHED_FLAG","SUSPECT_REPORTED_AGE", "SUSPECT_SEX",
         "SUSPECT_RACE_DESCRIPTION","STOP_LOCATION_PRECINCT" ]
new_col=[
    "year","month","inout", "crimsusp","arstmade", "explnstp", 
         "frisked", "searched", "age","sex", "race", "pct"
        ]
sqf_17.rename(columns=dict(zip(old_col, new_col)), inplace=True)





##########################################################################################
#look into how to make dframes!
dframes = pd.concat(sqf.values(), axis=0, ignore_index=True)

dframes= dframes.iloc[:,[0,12,1,3,4,5,6,7,8,9,10,11]] 
#dropped datestop by not including no 2 cause we don't need it lol
sqf_16 = sqf_16.iloc[:,[0,12,2,3,4,5,6,7,8,9,10,11]]
#threw out 1 cause we do not need datestop lololol
sqf_17=sqf_17.iloc[:,[0,1,11,2,3,4,5,6,7,9,10, 8]]
#changed order of 17 according to dframes so no probs with concat
dfList = [dframes,sqf_16, sqf_17]  # List of your dataframes
dframes = pd.concat(dfList, axis=0,ignore_index=True)




dframes['pct'] = dframes['pct'].replace(' ', np.NaN)
dframes['age'] = dframes['age'].replace([' ', '**', '(null)'], np.NaN)
dframes["age"] = pd.to_numeric(dframes["age"])
dframes["year"] = pd.to_numeric(dframes["year"]) #needed to change it for it to work
dframes = dframes[dframes['age']>15]
dframes["crimsusp"]=dframes["crimsusp"].replace(['^\s*$',"nan"],"none", regex=True)
#replaced empty values for "suspected crime" to none
dframes.drop(dframes.loc[dframes['pct'] > 123].index, inplace=True)
#deleted pcts over 123 because they go up to 123, rest makes 0 sense
dframes=dframes.reset_index(drop=True)
dframes.dropna(inplace=True)   

print( dframes.isnull().any())
#######################################################################################
#####################################################################################
#to do: check in on districts cause I cannot see 32!!
##################
#make sure to have same "race" name as for grad_rate so that you can use each race as a dummy 
#turning it off and on like a switch
valz = ['X', 'Z','(null)', 'U']
dframes = dframes[dframes.race.isin(valz) == False]

change_val = {'W':'White', 'Q':'Hispanic', 'B':'Black', 
              'A':'Asian/Pacific Islander', 
              'I':'American Indian/Alaska Native', 
              'WHITE HISPANIC':'Hispanic', 'BLACK':'Black',
              'BLACK HISPANIC':'Hispanic', 'WHITE':'White', 
              'ASIAN/PAC.ISL':'Asian/Pacific Islander', 
              'AMER IND':'American Indian/Alaska Native',
              'P': 'Hispanic'}

dframes["race"] = dframes["race"].replace(change_val)
#make sure to have sex also in order
more_valz = [ 'Z','(null)']
dframes = dframes[dframes.sex.isin(valz) == False]

chng_vls = {
             'MALE':'M', 'FEMALE':'F'
            }

dframes["sex"] = dframes["sex"].replace(chng_vls)

dframes= dframes[dframes.age < 22]
#have to adjust month column

dict_month = {
               'February': 2, 'March':3, 'April':4, 'September':9, 'October':10, 
               'January':1,'May':5, 'July':7, 'August':8, 'November':11, 
               'December':12, 'June':6 
            }
dframes["month"] = dframes["month"].replace(dict_month)

dframes["month"] = pd.to_numeric(dframes["month"])

del_val = [ '', '(null)']
dframes = dframes[dframes.inout.isin(del_val) == False]


#save this mofo real fast
dframes.to_csv('all_sqf.csv',index=False)
#have created now csv file uh yeah better to work with that now!

##################################################################################

#can now just import csv of "all_sqf"

dframes=pd.read_csv("all_sqf.csv",index_col=False)

year_count = dframes["year"].value_counts().reset_index()
year_count.columns = ["year", "count"]
year_count = year_count.sort_values(by="year")

sns.set_theme(style="darkgrid")
sns.lineplot(data=year_count, x= "year", y="count") 

plt.xlabel("Year")
plt.ylabel("Count", labelpad=10)
plt.title("Count of SQF Policing for Each Year")

  


plt.savefig('sqf_plot.png', dpi=300)  # Save the plot to a file named "your_plot.png" with 300 dpi


# sqf gradually got more and more over time with the biggest peek at 2011
#followed by a drop in 2012 and an even bigger one for the following years
#maybe connected to the courtcase?????

url = 'https://raw.githubusercontent.com/dwillis/nyc-maps/master/school_districts.geojson'

school_districts = gpd.read_file(url)

school_districts.to_file("school_districts.geojson", driver="GeoJSON")

url_pct = 'https://raw.githubusercontent.com/dwillis/nyc-maps/master/police_precincts.geojson'

police_precinct= gpd.read_file(url_pct)

joined = gpd.overlay(school_districts, police_precinct, how='intersection')

p = police_precinct.boundary.plot()
p.axis('off')
plt.savefig('pct.png', dpi=300)

s = school_districts.boundary.plot()
s.axis('off')
plt.savefig('dstrct.png', dpi=300)

j = joined.plot()
j.axis('off')
plt.savefig('jnd.png', dpi=300)
#we could use geopandas, however, since we are only interested in highschools 
#we will have to use my own made dictionary. this dictionary with joined however
#does portray all schools (so elementery up to hs)
#however could use this dictionary later on?

#the old dictionary has problems because the pcts overlap by being in multiple 
#districts. one way to go on about this is to shorten it to the "main" precincts 
#this would look like this:
    

d = {
       f'NYC GEOG DIST {i}' : f'{i}'
         for i in range(1, 33)
         }
all_reports['DISTRICT_NAME'] = all_reports['DISTRICT_NAME'].replace(d, regex=True)



older_col=["YEAR", "DISTRICT_NAME" ]
newer_col=[ 
    "year","district"
        ]
all_reports.rename(columns=dict(zip(older_col, newer_col)), inplace=True)

#sqf_with_regents= pd.merge(dframes, all_reports, on=["year", "pct"])

dframes['pct'] = pd.to_numeric(dframes['pct'])#cause is numeric with report card
#df too


pct_to_dstrct = {
     7 : '1',
     13: '2',
     20: '3', 
     23: '4',
     32: '5',
     34: '6',
     40: '7',
     41: '8',
     42: '9',
     48: '10',
     49: '11',
     43: '12', 
     84: '13', 
     90: '14',       
     76: '15', 
     81: '16',
     71: '17', 
     69: '18', 
     75: '19', 
     68: '20', 
     60: '21', 
     61: '22', 
     73: '23', 
     108: '24', 
     109: '25', 
     111: '26', 
     101: '27', #picked 101 cause no one has it
     107: '28',
     105: '29', 
     114: '30',  
     122: '31', 
     83: '32'
     }
#pct:dis



dframes['district'] = dframes['pct'].map(pct_to_dstrct) 
#works just save dframes for pxt as numeric to csv beforehand, also look into how you could merge etc..

#2 ideas: aggregation or just multiple rows with the 2 other districts that map
#to the given precinct
dframes.dropna(inplace=True) 

  #had to drop quite a bit because we can only 
#make sense of precincts that we can map onto school districts
#starting to merge now

#sqf_with_regents = pd.merge(dframes, all_reports, how="inner", on=["year", "district"])
#doesn't work due to memory issues


#############################################################################
#loading grad rate data
col_grad_08 =["Name", "subgroup", "%Graduated", "%IEP",
              "%Still Enrolled", "%Transferred to AHSEPP", "%Dropped Out"]

gradrate_08 = pd.read_excel("graduation_rate_2008.xlsx", usecols=col_grad_08,
                            index_col=False )

gradrate_08.rename(columns={'Name':'DISTRICT_NAME'}, inplace=True)

col_grad_09 =["DISTRICT_NAME" , "subgroup", "%Graduated", "%IEP", 
              "%Still Enrolled", "%Transferred to AHSEPP", "%Dropped Out"]

gradrate_09 = pd.read_excel("graduation_rate_2009.xlsx", usecols=col_grad_09,
                            index_col=False )

col_grad_10 =["DISTRICT_NAME" ,"SUBGROUP_NAME" , "Graduate%", "IEPDiploma%", 
              "StillEnrolled%", "XferGED%", "DroppedOut%"]
col_grad_15 = ["AGGREGATION_NAME","SUBGROUP_NAME", "GRAD_PCT", 
               "NON_DIPLOMA_CREDENTIAL_PCT" ,"STILL_ENR_PCT","GED_PCT",
               "DROPOUT_PCT"]

grads={}
for year in range (2010,2018):
    if year in range(2010,2015):
            grad_name = 'graduation_rate_' + str(year)+'.xlsx'
            grads[year] = pd.read_excel(grad_name, usecols=col_grad_10,
                                        index_col=False)
            grads[year] = grads[year].applymap(
                lambda x: x.strip() if isinstance(x, str) else x)
            grads[year].dropna(inplace=True)
    elif year in range (2015,2018):
            grad_name = 'graduation_rate_' + str(year)+'.csv'
            grads[year] = pd.read_csv(grad_name, usecols=col_grad_15,
                                      index_col=False)
            grads[year] = grads[year].applymap(
                lambda x: x.strip() if isinstance(x, str) else x)
           
    
gradrate_10 = grads[2010]
gradrate_11 = grads[2011]
gradrate_12 = grads[2012]
gradrate_13 = grads[2013]
gradrate_14 = grads[2014]
gradrate_15 = grads[2015]
gradrate_16 = grads[2016]
gradrate_17 = grads[2017]


for year in range (2015,2018):
    grad_name = 'gradrate_' + str(year)[-2:] 
    locals()[grad_name].rename(columns={'AGGREGATION_NAME':'DISTRICT_NAME'}, inplace=True)

district_values = [f"New York City Geographic District # {i}" for i in range(1, 10)] + [f"New York City Geographic District #{i}" for i in range(10, 33)]
district_values_11 = [f"NYC GEOG DIST # {i}" for i in range(1, 10)] + [f"NYC GEOG DIST #{i}" for i in range(10, 33)]






for year in range(2011, 2014):
    grad_name = 'gradrate_' + str(year)[-2:] 
    district_values = [f"New York City Geographic District # {i}" for i in range(1, 10)] + [f"New York City Geographic District #{i}" for i in range(10, 33)]
    locals()[grad_name]['DISTRICT_NAME'] = locals()[grad_name]['DISTRICT_NAME'].str.slice(0, 17)







district_values = [
    f"New York City Geographic District # {i}" for i in range(1, 10)
    ] + [
    f"New York City Geographic District #{i}" for i in range(10, 33)
] 
        
district_values_11 = [
    f"NYC GEOG DIST # {i}" for i in range(1, 10)
    ] + [
    f"NYC GEOG DIST #{i}" for i in range(10, 33)
]         
        
district_values_15 = [
    f"NEW YORK CITY GEOGRAPHIC DISTRICT # {i}" for i in range(1, 10)
    ] + [
    f"NEW YORK CITY GEOGRAPHIC DISTRICT #{i}" for i in range(10, 33)
] 
          

gradrate_08 = gradrate_08[gradrate_08['DISTRICT_NAME'].isin(district_values)]
gradrate_09 = gradrate_09[gradrate_09['DISTRICT_NAME'].isin(district_values)]
gradrate_10 = gradrate_10[gradrate_10['DISTRICT_NAME'].isin(district_values)]

gradrate_11 = gradrate_11[gradrate_11['DISTRICT_NAME'].isin(district_values_11)]
gradrate_12 = gradrate_12[gradrate_12['DISTRICT_NAME'].isin(district_values_11)]
gradrate_13 = gradrate_13[gradrate_13['DISTRICT_NAME'].isin(district_values_11)]

gradrate_14 = gradrate_14[gradrate_14['DISTRICT_NAME'].isin(district_values)]

gradrate_15 = gradrate_15[gradrate_15['DISTRICT_NAME'].isin(district_values_15)]
gradrate_16 = gradrate_16[gradrate_16['DISTRICT_NAME'].isin(district_values_15)]
gradrate_17 = gradrate_17[gradrate_17['DISTRICT_NAME'].isin(district_values_15)]


#add year column
for year in range(2008,2018):
    grad_name = 'gradrate_' + str(year)[-2:] 
    locals()[grad_name].insert(0,"year", year)
    

for year in range (2008,2010):
    grad_name = 'gradrate_' + str(year)[-2:] 
    locals()[grad_name].rename(columns={'subgroup':'SUBGROUP_NAME'}, inplace=True)


              

    old_columns_17=[ 'GRAD_PCT','NON_DIPLOMA_CREDENTIAL_PCT', 'STILL_ENR_PCT', 
                    'GED_PCT','DROPOUT_PCT']
    old_columns_16=['GRAD_PCT','NON_DIPLOMA_CREDENTIAL_PCT', 'STILL_ENR_PCT', 
                    'GED_PCT','DROPOUT_PCT']
    old_columns_15=['GRAD_PCT','NON_DIPLOMA_CREDENTIAL_PCT', 'STILL_ENR_PCT', 
                    'GED_PCT','DROPOUT_PCT']
    old_columns_15=['GRAD_PCT','NON_DIPLOMA_CREDENTIAL_PCT', 'STILL_ENR_PCT', 
                    'GED_PCT','DROPOUT_PCT']
    new_columns=["Graduate%", "IEPDiploma%", 
                  "StillEnrolled%", "XferGED%", "DroppedOut%"]
gradrate_17.rename(columns=dict(zip(old_columns_17, new_columns)), inplace=True)
gradrate_16.rename(columns=dict(zip(old_columns_16, new_columns)), inplace=True)
gradrate_15.rename(columns=dict(zip(old_columns_15, new_columns)), inplace=True)

old_columns_08=['%Graduated', '%IEP','%Still Enrolled', '%Dropped Out']
new_columns_08=["Graduate%", "IEPDiploma%", "StillEnrolled%", "DroppedOut%"]

gradrate_08.rename(columns=dict(zip(old_columns_08, new_columns_08)), inplace=True)
gradrate_09.rename(columns=dict(zip(old_columns_08, new_columns_08)), inplace=True)



gradrate_11['DISTRICT_NAME']=gradrate_11['DISTRICT_NAME'].str.slice(15,17)
gradrate_12['DISTRICT_NAME']=gradrate_12['DISTRICT_NAME'].str.slice(15,17)
gradrate_13['DISTRICT_NAME']=gradrate_13['DISTRICT_NAME'].str.slice(15,17)

gradrate_10['DISTRICT_NAME']=gradrate_10['DISTRICT_NAME'].str.slice(35,37)
gradrate_14['DISTRICT_NAME']=gradrate_14['DISTRICT_NAME'].str.slice(35,37)
gradrate_15['DISTRICT_NAME']=gradrate_15['DISTRICT_NAME'].str.slice(35,37)
gradrate_16['DISTRICT_NAME']=gradrate_16['DISTRICT_NAME'].str.slice(35,37)
gradrate_17['DISTRICT_NAME']=gradrate_17['DISTRICT_NAME'].str.slice(35,37)



gradrate_10["DISTRICT_NAME"]=pd.to_numeric(gradrate_10["DISTRICT_NAME"])
gradrate_11["DISTRICT_NAME"]=pd.to_numeric(gradrate_11["DISTRICT_NAME"])
gradrate_12["DISTRICT_NAME"]=pd.to_numeric(gradrate_12["DISTRICT_NAME"])
gradrate_13["DISTRICT_NAME"]=pd.to_numeric(gradrate_13["DISTRICT_NAME"])
gradrate_14["DISTRICT_NAME"]=pd.to_numeric(gradrate_14["DISTRICT_NAME"])
gradrate_15["DISTRICT_NAME"]=pd.to_numeric(gradrate_15["DISTRICT_NAME"])
gradrate_16["DISTRICT_NAME"]=pd.to_numeric(gradrate_16["DISTRICT_NAME"])
gradrate_17["DISTRICT_NAME"]=pd.to_numeric(gradrate_17["DISTRICT_NAME"])

    


#look into each dfs columns and see which should be removed and match who
#took from 10 onwards because no idea how to match ahsepp to ged 
graduation_list = [gradrate_10, gradrate_11,
                   gradrate_12, gradrate_13, gradrate_14, gradrate_15,
                   gradrate_16, gradrate_17 ] 

graduation_rate = pd.concat(graduation_list , axis=0,ignore_index=True)

graduation_rate['Graduate%'] = graduation_rate['Graduate%'].replace('#', np.NaN)
graduation_rate=graduation_rate.dropna().reset_index(drop=True)



graduation_rate.rename(columns={'DISTRICT_NAME':'district'}, inplace=True)

#dropping values that I cannot merge with sqf data and therefore need to drop
val = ['All Students',
       'General Education Students',
       'Students with Disabilities', 'Economically Disadvantaged',
       'Not Economically Disadvantaged', 'Female', 'Male',
       'Multiracial', 'Not Limited English Proficient',
       'Formerly Limited English Proficient', 'Not Migrant',
       'Limited English Proficient', 
       'Non-English Language Learners',
       'English Language Learners', 'Not English Language Learner',
       'English Language Learner']
graduation_rate = graduation_rate[graduation_rate.SUBGROUP_NAME.isin(val) == False]

#merging these togetehr to one because it is practically the same and the excel
#doesn't give too much info about the differences between these two
old_to_new = {'American Indian or Alaska Native':'American Indian/Alaska Native', 
           'Black or African American': 'Black', 
           'Asian or Pacific Islander': 'Asian/Pacific Islander',
           'Hispanic or Latino': 'Hispanic'}

graduation_rate["SUBGROUP_NAME"] = graduation_rate["SUBGROUP_NAME"].replace(old_to_new)

graduation_rate.rename(columns={'SUBGROUP_NAME':'race'}, inplace=True)
graduation_rate = graduation_rate[graduation_rate["DroppedOut%"] != '-']
graduation_rate["Graduate%"] = graduation_rate["Graduate%"].replace('None', pd.NaT)#explain
graduation_rate = graduation_rate.dropna(subset=["Graduate%"])

graduation_rate.to_csv('graduation_rate.csv',index=False)


def change(row):
  graduate_rate = row["DroppedOut%"]
  
  if isinstance(graduate_rate, str):
      if graduate_rate.endswith('%'):
          graduate_rate = graduate_rate[:-1]
      
      graduate_rate = pd.to_numeric(graduate_rate) / 100
  
  row["DroppedOut%"] = graduate_rate
  return row

graduation_rate = graduation_rate.apply(change, axis=1)#using apply to use my previous built function


def change_again(row):
    graduate_rate = row["Graduate%"]
    
    if isinstance(graduate_rate, str):
        if graduate_rate.endswith('%'):
            graduate_rate = graduate_rate[:-1]
        
        graduate_rate = pd.to_numeric(graduate_rate) / 100
    
    row["Graduate%"] = graduate_rate
    return row

graduation_rate = graduation_rate.apply(change_again, axis=1)








def change_again1(row):
  graduate_rate = row["IEPDiploma%"]
  
  if isinstance(graduate_rate, str):
      if graduate_rate.endswith('%'):
          graduate_rate = graduate_rate[:-1]
      
      graduate_rate = pd.to_numeric(graduate_rate) / 100
  
  row["IEPDiploma%"] = graduate_rate
  return row

graduation_rate = graduation_rate.apply(change_again1, axis=1)

def change_again2(row):
  graduate_rate = row["StillEnrolled%"]
  
  if isinstance(graduate_rate, str):
      if graduate_rate.endswith('%'):
          graduate_rate = graduate_rate[:-1]
      
      graduate_rate = pd.to_numeric(graduate_rate) / 100
  
  row["StillEnrolled%"] = graduate_rate
  return row

graduation_rate = graduation_rate.apply(change_again2, axis=1)

def change_again3(row):
  graduate_rate = row["XferGED%"]
  
  if isinstance(graduate_rate, str):
      if graduate_rate.endswith('%'):
          graduate_rate = graduate_rate[:-1]
      
      graduate_rate = pd.to_numeric(graduate_rate) / 100
  
  row["XferGED%"] = graduate_rate
  return row

graduation_rate = graduation_rate.apply(change_again3, axis=1)




graduation_rate.to_csv('graduation_rate.csv',index=False)
#have created now csv file uh yeah better to work with that now!
blep=pd.read_csv("report_card_2012.csv",index_col=False)
graduation_rate=pd.read_csv("graduation_rate.csv",index_col=False)
####################merge dem mofos
dframes["district"] = pd.to_numeric(dframes["district"])
sqf_w_grad_rate = pd.merge(dframes, graduation_rate, how="inner", on=["district", "year", "race"])



print(sqf_w_grad_rate.isnull().values.any())    
#just to check but false so yay

sqf_w_grad_rate.to_csv('sqf_w_grad_rate.csv',index=False)
sqf_w_grad_rate=pd.read_csv("sqf_w_grad_rate.csv",index_col=False)

minority_pct = [23, 32, 40, 41, 43, 49, 69, 71, 73, 75, 81, 83, 105]
blck_pct = [23, 32, 40, 43, 49, 69, 71, 73, 75, 81, 83, 105]

sqf_w_grad_rate["post_12"] = (sqf_w_grad_rate["year"]>= 2012).astype(int) #so evertyhing after 12 is 1 and else 0
sqf_w_grad_rate["black"] = (sqf_w_grad_rate["race"]=="Black").astype(int)
sqf_w_grad_rate["black_neighborhood"] = sqf_w_grad_rate["pct"].apply(lambda x: 1 if x in blck_pct else 0)

######################################delete
sqf_w_grad_rate["hispanic"] = (sqf_w_grad_rate["race"]=="Hispanic").astype(int)
sqf_w_grad_rate["asian"] = (sqf_w_grad_rate["race"]=="Asian/Pacific Islander").astype(int)
sqf_w_grad_rate["male"] = (sqf_w_grad_rate["sex"]=="M").astype(int)
sqf_w_grad_rate["white"] = (sqf_w_grad_rate["race"]=="White").astype(int)

minority = ["Black", "Hispanic"]

sqf_w_grad_rate["minority"] = sqf_w_grad_rate["race"].apply(lambda x: 1 if x in minority else 0)
sqf_w_grad_rate["white_neighborhood"] = sqf_w_grad_rate["pct"].apply(lambda x: 0 if x in blck_pct else 1)
sqf_w_grad_rate["minority_neighborhood"] = sqf_w_grad_rate["pct"].apply(lambda x: 1 if x in minority_pct else 0)
############################################################################
################################################################

#creating new columns where I will have average dropouts, graduates etc. so 
#that I can shorten my df to 64xn 


def extract_means(main_df, case):
    "This will compute the means for the case described"
    for year in range(2010, 2018):
        for district in range(1, 33):
            condition1 = (main_df["year"] == year) & (main_df["district"] == district) & (main_df["post_12"] == 0)  & (main_df["black"] == 0)
            condition2 = (main_df["year"] == year) & (main_df["district"] == district) & (main_df["post_12"] == 0)  & (main_df["black"] == 1)
            condition3 = (main_df["year"] == year) & (main_df["district"] == district) & (main_df["post_12"] == 1)  & (main_df["black"] == 0)
            condition4 = (main_df["year"] == year) & (main_df["district"] == district) & (main_df["post_12"] == 1)  & (main_df["black"] == 1)
            
            filtered_df_0 = main_df[condition1]
            filtered_df_1 = main_df[condition2]
            filtered_df_2 = main_df[condition3]
            filtered_df_3 = main_df[condition4]
            
            average_dropout_0 = np.average(filtered_df_0[case])
            average_dropout_1 = np.average(filtered_df_1[case])
            average_dropout_2 = np.average(filtered_df_2[case])
            average_dropout_3 = np.average(filtered_df_3[case])
            
            col_name = "average_{}".format(case)
            main_df.loc[condition1, col_name] = average_dropout_0
            main_df.loc[condition2, col_name] = average_dropout_1
            main_df.loc[condition3, col_name] = average_dropout_2
            main_df.loc[condition4, col_name] = average_dropout_3
    return sqf_w_grad_rate
            
sqf_w_grad_rate = extract_means(sqf_w_grad_rate, "DroppedOut%")
sqf_w_grad_rate = extract_means(sqf_w_grad_rate, "Graduate%")
sqf_w_grad_rate = extract_means(sqf_w_grad_rate, "XferGED%")
sqf_w_grad_rate = extract_means(sqf_w_grad_rate, "IEPDiploma%")

##########################
#save so no need for re running code all over again
#time to shorten matrix!
#let's create one with only the columns we need!
sqf_w_grad_rate.to_csv('sqf_w_grad_rate.csv',index=False)
sqf_w_grad_rate=pd.read_csv("sqf_w_grad_rate.csv",index_col=False)
sqf_w_grad_rate = sqf_w_grad_rate.rename(columns=
    {"average_DroppedOut%" : "average_dropouts",
     "average_Graduate%" : "average_graduates",
     "average_XferGED%" : "average_GED",
     "average_IEPDiploma%" : "average_IEPD"
     })


short_sqf_grads = sqf_w_grad_rate.loc[:,['year','district' , 'pct', 'post_12',
                                       'black', 
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD']]

# delete columns for which black_neighborhood=1 but black=0 and vice versa
#dropping all columns were black neighborhood and black don't share a common value 
#because otherwise it makes no sense


#for each year and district and post12==1 and or ==0 just give me one column if 
#grad average is the same
#simplest way to do so is to remove duplicates!

short_sqf_grads =    short_sqf_grads.drop_duplicates(['year','district' , 'pct', 'post_12',
                                       'black', 
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD'])

short_sqf_grads.to_csv('short_sqf_grads.csv',index=False)

#########################################################################################################

# Plotting the means over time
ptrends_df = short_sqf_grads.groupby(["year", "black"]).agg("mean").reset_index()
black_df   = ptrends_df[ptrends_df["black"] == 1][['average_dropouts', 'average_graduates', 'average_GED', 'average_IEPD']]
white_df   = ptrends_df[ptrends_df["black"] == 0][['average_dropouts', 'average_graduates', 'average_GED', 'average_IEPD']]

for df in [black_df, white_df]:
    df["year"] = range(2010, 2018)

plt.plot(black_df["year"], black_df["average_dropouts"], label="Black Adolescents")
plt.plot(white_df["year"], white_df["average_dropouts"],  label="White Adolescents")
cutoff = 2012
plt.axvline(x=cutoff, color='grey', linestyle='--', label='Beginning of Reform')
plt.xlabel('Year')
plt.ylabel('Average Dropouts')
plt.legend()
plt.title('Parallel Trends Assumption with Cutoff')
plt.savefig('parallelplot.png', dpi=300)
plt.show()





##############################################################
regr = 'average_dropouts ~ post_12 + black + post_12*black'

Y_train, X_train = dmatrices(regr, short_sqf_grads, return_type="dataframe")


did_regr = sm.OLS(endog=Y_train, exog=X_train)

#training the model
did_regr_trained = did_regr.fit(cov_type="HC0")


did_regr_trained.summary()
#just scatterplot
plt.scatter(short_sqf_grads["year"], Y_train)
plt.title("DiD Regression")
plt.xlabel("year")
plt.ylabel("Average Dropouts")
plt.show()

#scatterplot with line
year = short_sqf_grads["year"]
plt.plot(year, Y_train, 'o', color='blue')
plt.title("Basic DiD Regression")
m, b = np.polyfit(year, Y_train,1)
plt.plot(year, m*year+b, color= "red")

plt.savefig('regr1plot.png', dpi=300)

#a clear downward trend is to be seen
#due to our r^2 being so low it only explains roughly 10% of the variance in 
#for the average dropouts (our endog variable)
#due to f stat being over 2 which is highly significant,
#leading one to believe that the model's variables are jointly significant 
#and doing a good job at explaining the average dropout than a simple mean model would
#except for interaction effect which has p value > 0.05 the rest is significant


#E(average_dropout) is 0.1515, so for the control group,
#e.g. people in non black neighborhoods the estimated average 
#dropout is at 15.15%
#since non-black neighborhoods also contains latino 
#neighborhoods, this would beg the question if this "high"
#percentage is due to that
#post=1, black neighborhood=0
#0.1515-0.0226 = 0.1289

#the avg. drop out rate for control group post 12 
#o after floyd reform dropped to 12,89%

#post=0, blck neighborhood=1
#0.1515+0.0271 = 0.1786

#the avg. drop out rate for treatment group pre floyd reform 
#was at 17,86%


#post=1, blck neighborhood=1
#the avg dropout for treatment post floyd reform
#0.1515-0.0226+0.0271-0.0103=0.1457
#is at 14,57% so still higher than control


#the did effect between the two groups is:
   #    treat group         control group 
#time=0    0.1786                0.1515

#     1    0.1457                   0.1289

#---------------------------------------------
#        -0.0329                 -0.0226


#-> -0.0329-(-0.0226) = -0.0103 -> -1,03%
#exactly the interaction value we have for our trained model huehue
#here the programmed version:


# Compute the four data points needed in the DID calculation:
a = short_sqf_grads.loc[(short_sqf_grads['post_12'] == 0) & (short_sqf_grads["black"] == 0), 'average_dropouts'].mean()
b = short_sqf_grads.loc[(short_sqf_grads['post_12'] == 0) & (short_sqf_grads["black"] == 1), 'average_dropouts'].mean()
c = short_sqf_grads.loc[(short_sqf_grads['post_12'] == 1) & (short_sqf_grads["black"] == 0), 'average_dropouts'].mean()
d = short_sqf_grads.loc[(short_sqf_grads['post_12'] == 1) & (short_sqf_grads["black"] == 1), 'average_dropouts'].mean()

# Compute the effect of the floyd reform on the dropout of black adolescents
effect = (d - c) - (b - a)
#is at 0.00108864 So 0,11% dropped out due to new reform 

#bigger question: sure it is not much but is it much regarding the AMOUNT of black folks that are in ny?

#effect is pretty small, this is because there isn't a big balance because
#more people graduate than drop out

#########################################################################################
short_sqf_grads_male = sqf_w_grad_rate.loc[:,['year','district' , 'pct', 'post_12',
                                       'black','male', 
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD']]



short_sqf_grads_male =    short_sqf_grads_male.drop_duplicates(['year','district' , 'pct', 'post_12',
                                       'black', 'male', 
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD'])



regr_male = 'average_dropouts ~ post_12 + male + black + post_12*black'

Y_train4, X_train4 = dmatrices(regr_male, short_sqf_grads_male, return_type="dataframe")


did_regr4 = sm.OLS(endog=Y_train4, exog=X_train4)

#training the model
did_regr_trained4 = did_regr4.fit(cov_type="HC0")


did_regr_trained4.summary() #managed to lower SE, question: is this linked to bigger datasize?
#just scatterplot
plt.scatter(short_sqf_grads_male["year"], Y_train4)
plt.title("DiD Regression with Male")
plt.xlabel("year")
plt.ylabel("Average Dropouts")
plt.show()

#scatterplot with line
year4 = short_sqf_grads_male["year"]
plt.plot(year4, Y_train4, 'o', color='blue')
m4, b4 = np.polyfit(year4, Y_train4,1)
plt.title("DiD Regression with Male")
plt.plot(year4, m4*year4+b4, color= "red")

plt.savefig('regr2plot.png', dpi=300)




########## add neighborhood
short_sqf_grads_nei = sqf_w_grad_rate.loc[:,['year','district' , 'pct', 'post_12',
                                       'black','male', 'black_neighborhood',
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD']]



short_sqf_grads_nei =    short_sqf_grads_nei.drop_duplicates(['year','district' , 'pct', 'post_12',
                                       'black', 'male', 'black_neighborhood',
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD'])


regr_neighb = 'average_dropouts ~ post_12 + male + black_neighborhood + black + post_12*black'

Y_train5, X_train5 = dmatrices(regr_neighb, short_sqf_grads_nei, return_type="dataframe")


did_regr5 = sm.OLS(endog=Y_train5, exog=X_train5)

#training the model
did_regr_trained5 = did_regr5.fit(cov_type="HC0")


did_regr_trained5.summary() #managed to lower SE, question: is this linked to bigger datasize?
#just scatterplot
plt.scatter(short_sqf_grads_nei["year"], Y_train5)
plt.title("DiD Regression male neighbor black")
plt.xlabel("year")
plt.ylabel("Average Dropouts")
plt.show()

#scatterplot with line
year5 = short_sqf_grads_nei["year"]
plt.plot(year5, Y_train5, 'o', color='blue')
m5, b5 = np.polyfit(year5, Y_train5,1)
plt.title("DiD Regression with three dummies")
plt.plot(year5, m5*year5+b5, color= "red")

plt.savefig('regr3plot.png', dpi=300)




stargazer = Stargazer([did_regr_trained, did_regr_trained4, did_regr_trained5])
stargazer1 = Stargazer([ did_regr_trained2, did_regr_trained6, did_regr_trained7, ])

stargazer.render_latex()
stargazer1.render_latex() #using stargazer to compile the given lateX code for me to show regression
################################################################################################



#do same thing but instead of black use "minority"
short_sqf_grads_minority = sqf_w_grad_rate.loc[:,['year','district' , 'pct', 'post_12',
                                       'minority',  
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD']]

short_sqf_grads_minority =    short_sqf_grads_minority.drop_duplicates(['year','district' , 'pct', 'post_12',
                                       'minority',  
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD'])




regr_minority = 'average_dropouts ~ post_12 + minority + post_12*minority'

Y_train2, X_train2 = dmatrices(regr_minority, short_sqf_grads_minority, return_type="dataframe")


did_regr2 = sm.OLS(endog=Y_train2, exog=X_train2)

#training the model
did_regr_trained2 = did_regr2.fit()


did_regr_trained2.summary() #minority basic
#a lot better at explaining shit
#just scatterplot
plt.scatter(short_sqf_grads_minority["year"], Y_train2)
plt.title("DiD Regression minority")
plt.xlabel("year")
plt.ylabel("Average Dropouts")
plt.show()

#scatterplot with line
year2 = short_sqf_grads_minority["year"]
plt.plot(year2, Y_train2, 'o', color='blue')
plt.title("DiD Regression minority")
m2, b2 = np.polyfit(year2, Y_train2,1)
plt.plot(year2, m2*year2+b2, color= "red")

##########################################################################
#minority is worse off    
short_sqf_grads_minority10 = sqf_w_grad_rate.loc[:,['year','district' , 'pct', 'post_12',
                                       'minority',  'male',
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD']]

short_sqf_grads_minority10 =    short_sqf_grads_minority10.drop_duplicates(['year','district' , 'pct', 'post_12',
                                       'minority',  'male',
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD'])



regr_minority2 = 'average_dropouts ~ post_12 + male + minority + post_12*minority'

Y_train6, X_train6 = dmatrices(regr_minority2, short_sqf_grads_minority10, return_type="dataframe")


did_regr6 = sm.OLS(endog=Y_train6, exog=X_train6)

#training the model
did_regr_trained6 = did_regr6.fit()


did_regr_trained6.summary() #minority basic
#a lot better at explaining shit
#just scatterplot
plt.scatter(short_sqf_grads_minority10["year"], Y_train6)
plt.title("DiD Regression minority")
plt.xlabel("year")
plt.ylabel("Average Dropouts")
plt.show()

#scatterplot with line
year6 = short_sqf_grads_minority10["year"]
plt.plot(year6, Y_train6, 'o', color='blue')
plt.title("DiD Regression minority w male")
m6, b6 = np.polyfit(year6, Y_train6,1)
plt.plot(year6, m6*year6+b6, color= "red")

##########################################################################
#minority is worse off    
short_sqf_grads_minority1 = sqf_w_grad_rate.loc[:,['year','district' , 'pct', 'post_12','male',
                                       'minority', 'minority_neighborhood', 
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD']]

#for each year and district and post12==1 and or ==0 just give me one column if 
#grad average is the same
#simplest way to do so is to remove duplicates!

short_sqf_grads_minority1 =    short_sqf_grads_minority1.drop_duplicates(['year','district' , 'pct', 'post_12',
                                       'minority', 'minority_neighborhood', 'male',
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD'])


regr_minority3 = 'average_dropouts ~ post_12 + male + minority + minority_neighborhood + post_12*minority'

Y_train7, X_train7 = dmatrices(regr_minority3, short_sqf_grads_minority1, return_type="dataframe")


did_regr7 = sm.OLS(endog=Y_train7, exog=X_train7)

#training the model
did_regr_trained7 = did_regr7.fit()


did_regr_trained7.summary() #minority basic
#a lot better at explaining shit
#just scatterplot
plt.scatter(short_sqf_grads_minority1["year"], Y_train7)
plt.title("DiD Regression minority full")
plt.xlabel("year")
plt.ylabel("Average Dropouts")
plt.show()

#scatterplot with line
year7 = short_sqf_grads_minority1["year"]
plt.plot(year7, Y_train7, 'o', color='blue')
plt.title("DiD Regression minority full")
m7, b7 = np.polyfit(year7, Y_train7,1)
plt.plot(year7, m7*year7+b7, color= "red")



 
#####################################parallel trends assumption plotted###########################

#make same thing as above for "white" and "non minority"

 # delete columns for which black_neighborhood=1 but black=0 and vice versa



short_sqf_grads_white = sqf_w_grad_rate.loc[:,['year','district' , 'pct', 'post_12',
                                       'white', 
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD']]


#for each year and district and post12==1 and or ==0 just give me one column if 
#grad average is the same
#simplest way to do so is to remove duplicates!

short_sqf_grads_white =    short_sqf_grads_white.drop_duplicates(['year','district' , 'pct', 'post_12',
                                       'white',
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD'])



regr_white = 'average_dropouts ~ post_12 + white  +  post_12*white'

Y_train3, X_train3 = dmatrices(regr_white, short_sqf_grads_white, return_type="dataframe")


did_regr3 = sm.OLS(endog=Y_train3, exog=X_train3)

#training the model
did_regr_trained3 = did_regr3.fit()


did_regr_trained3.summary()
#a lot better at explaining shit
#just scatterplot
plt.scatter(short_sqf_grads_white["year"], Y_train3)
plt.title("DiD Regression")
plt.xlabel("year")
plt.ylabel("Average Dropouts")
plt.show()

#scatterplot with line
year3x = short_sqf_grads_white["year"]
plt.plot(year3x, Y_train3, 'o', color='blue')
m3, b3 = np.polyfit(year3x, Y_train3,1)
plt.title("DiD Regression white")
plt.plot(year3x, m3*year3x+b3, color= "purple")
##############################################################################
#white
short_sqf_grads_white1 = sqf_w_grad_rate.loc[:,['year','district' , 'pct', 'post_12',
                                       'white', 'male','white_neighborhood',
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD']]


#for each year and district and post12==1 and or ==0 just give me one column if 
#grad average is the same
#simplest way to do so is to remove duplicates!

short_sqf_grads_white1 =    short_sqf_grads_white1.drop_duplicates(['year','district' , 'pct', 'post_12',
                                       'white', 'male','white_neighborhood',
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD'])



regr_white1 = 'average_dropouts ~ post_12 + white + male + white_neighborhood +  post_12*white'

Y_train300, X_train300 = dmatrices(regr_white1, short_sqf_grads_white1, return_type="dataframe")


did_regr300 = sm.OLS(endog=Y_train300, exog=X_train300)

#training the model
did_regr_trained300 = did_regr300.fit()


did_regr_trained300.summary()
#a lot better at explaining shit
#just scatterplot
plt.scatter(short_sqf_grads_white1["year"], Y_train300)
plt.title("DiD Regression")
plt.xlabel("year")
plt.ylabel("Average Dropouts")
plt.show()

#scatterplot with line
year0 = short_sqf_grads_white1["year"]
plt.plot(year0, Y_train300, 'o', color='blue')
m300, b300 = np.polyfit(year0, Y_train300,1)
plt.title("DiD Regression white")
plt.plot(year0, m300*year0+b300, color= "red")
















#lez see difference with black)
plt.plot(year, m*year+b, color= "black", label= "Black adolescents") #black
plt.plot(year, m3*year+b3, color= "red", label="White adolescents")#white
cutoff = 2012
plt.axvline(x=cutoff, color='grey', linestyle='--', label='Beginning of Reform')
# Add labels, legend, and title
plt.xlabel('Year')
plt.ylabel('Average Dropouts')
plt.legend()
plt.title('Parallel Trends Assumption with Cutoff')
#plt.show()
plt.savefig('partrend.png', dpi=300)





plt.plot(year, m5*year+b5, color= "black", label= "Black adolescents") #black
plt.plot(year, m300*year+b300, color= "red", label="White adolescents")#white
cutoff = 2012
plt.axvline(x=cutoff, color='grey', linestyle='--', label='Beginning of Reform')
# Add labels, legend, and title
plt.xlabel('Year')
plt.ylabel('Average Dropouts')
plt.legend()
plt.title('Parallel Trends Assumption with Cutoff')
#plt.show()



#######################################################################


#############################
#/w FE

short_sqf_grads.set_index(['year','district'], inplace=True)

short_sqf_grads['post_12_black_interaction'] = short_sqf_grads['post_12'] * short_sqf_grads['black']

# Specify the regression formula
formula = 'average_dropouts ~ post_12 + black + post_12_black_interaction'

# Create the PanelOLS object with entity (fixed) effects for 'year' and 'district'
regFE = PanelOLS.from_formula(formula, data=short_sqf_grads)

# Fit the regression
reg_results = regFE.fit(cov_type='clustered', cluster_entity=True)

# Print the regression results
print(reg_results)

reg_table = reg_results.summary

# Print the LaTeX table
print(reg_table.as_latex())



############################################################

#do same thing but instead of black use "hispanic"
short_sqf_grads_hisp = sqf_w_grad_rate.loc[:,['year','district' , 'pct', 'post_12',
                                       'hispanic',  
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD']]

short_sqf_grads_hisp =    short_sqf_grads_hisp.drop_duplicates(['year','district' , 'pct', 'post_12',
                                       'hispanic',  
                                       'average_dropouts', 'average_graduates',
                                       'average_GED', 'average_IEPD'])




regr_hisp = 'average_dropouts ~ post_12 + hispanic + post_12*hispanic'

Y_trainH, X_trainH = dmatrices(regr_hisp, short_sqf_grads_hisp, return_type="dataframe")


did_regrH = sm.OLS(endog=Y_trainH, exog=X_trainH)

#training the model
did_regr_trainedH = did_regrH.fit()


did_regr_trainedH.summary() #minority basic
#a lot better at explaining shit
#just scatterplot
plt.scatter(short_sqf_grads_hisp["year"], Y_trainH)
plt.title("DiD Regression hispanic")
plt.xlabel("year")
plt.ylabel("Average Dropouts")
plt.show()

#scatterplot with line
yearH = short_sqf_grads_hisp["year"]
plt.plot(yearH, Y_trainH, 'o', color='blue')
plt.title("DiD Regression hispanic")
mH, bH = np.polyfit(yearH, Y_trainH,1)
plt.plot(yearH, mH*yearH+bH, color= "red")


########################################differences for blacks and minorities

plt.plot(year5, m5*year5+b5, color= "black", label="Blacks with 3 dummies")#black male neighborhood
plt.plot(year7, m7*year7+b7, color= "red", label="Minority with 3 dummies")#minority male neighborhood
plt.plot(year0, m300*year0+b300, color= "blue", label="White with 3 dummies")
# Add labels, legend, and title
plt.xlabel('Year')
plt.ylabel('Average Dropouts')
plt.legend()
plt.title("Differences Between Regressions only the race Dummy")
#plt.show()
plt.savefig('blackdif.png', dpi=300)



plt.plot(year, m*year+b, color= "black", label="Black with 1 Dummy")#black male neighborhood
plt.plot(year2, m2*year2+b2, color= "red", label="Minority with 1 Dummy")#minority male neighborhood
plt.plot(year3x, m3*year3x+b3, color= "blue", label="White with 1 Dummy")
# Add labels, legend, and title
plt.xlabel('Year')
plt.ylabel('Average Dropouts')
plt.legend()
#plt.show()
plt.savefig('dif1dif.png', dpi=300)






























