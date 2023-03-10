#!/usr/bin/env python
# coding: utf-8

# # Part I. ETL Pipeline for Pre-Processing the Files

# ## PLEASE RUN THE FOLLOWING CODE FOR PRE-PROCESSING THE FILES

# #### Import Python packages 

# In[2]:


# Import Python packages 
import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv


# #### Creating list of filepaths to process original event csv data files

# In[3]:


# checking your current working directory
print(os.getcwd())

# Get your current folder and subfolder event data
filepath = os.getcwd() + '/event_data'

# Create a for loop to create a list of files and collect each filepath
for root, dirs, files in os.walk(filepath):
    
# join the file path and roots with the subdirectories using glob
    file_path_list = glob.glob(os.path.join(root,'*'))
    #print(file_path_list)


# In[4]:


# Create a for loop to create a list of files and collect each filepath
for root, dirs, files in os.walk(filepath):
    
# join the file path and roots with the subdirectories using glob
    file_path_list = glob.glob(os.path.join(root,'*'))
    #print(file_path_list)


# #### Processing the files to create the data file csv that will be used for Apache Casssandra tables

# In[5]:


# initiating an empty list of rows that will be generated from each file
full_data_rows_list = [] 
    
# for every filepath in the file path list 
for f in file_path_list:

# reading csv file 
    with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
        # creating a csv reader object 
        csvreader = csv.reader(csvfile) 
        next(csvreader)
        
 # extracting each data row one by one and append it        
        for line in csvreader:
            #print(line)
            full_data_rows_list.append(line) 
            
# uncomment the code below if you would like to get total number of rows 
#print(len(full_data_rows_list))
# uncomment the code below if you would like to check to see what the list of event data rows will look like
#print(full_data_rows_list)

# creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
# Apache Cassandra tables
csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
    writer = csv.writer(f, dialect='myDialect')
    writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',                'level','location','sessionId','song','userId'])
    for row in full_data_rows_list:
        if (row[0] == ''):
            continue
        writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))


# In[6]:


# check the number of rows in your csv file
with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
    print(sum(1 for line in f))


# # Part II. Complete the Apache Cassandra coding portion of your project. 
# 
# ## Now you are ready to work with the CSV file titled <font color=red>event_datafile_new.csv</font>, located within the Workspace directory.  The event_datafile_new.csv contains the following columns: 
# - artist 
# - firstName of user
# - gender of user
# - item number in session
# - last name of user
# - length of the song
# - level (paid or free song)
# - location of the user
# - sessionId
# - song title
# - userId
# 
# The image below is a screenshot of what the denormalized data should appear like in the <font color=red>**event_datafile_new.csv**</font> after the code above is run:<br>
# 
# <img src="images/image_event_datafile_new.jpg">

# ## Begin writing your Apache Cassandra code in the cells below

# #### Creating a Cluster

# In[7]:


# This should make a connection to a Cassandra instance your local machine 
# (127.0.0.1)

from cassandra.cluster import Cluster
cluster = Cluster()

# To establish connection and begin executing queries, need a session
session = cluster.connect()


# #### Create Keyspace

# In[8]:


# TO-DO: Creatinf od Keyspace (database object that controls the replication of the object)

session.execute("""
                    create keyspace if not exists sparkify 
                    with replication = {'class': 'SimpleStrategy' , 'replication_factor': 1 }
                """)


# #### Set Keyspace

# In[27]:


# TO-DO: Connecting keyspace to sparkify 

session.set_keyspace('sparkify')


# ### Now we need to create tables to run the following queries. Remember, with Apache Cassandra you model the database tables on the queries you want to run.

# ## Create queries to ask the following three questions of the data
# 
# ### 1. Give me the artist, song title and song's length in the music app history that was heard during  sessionId = 338, and itemInSession  = 4
# 
# 
# ### 2. Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
#     
# 
# ### 3. Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
# 
# 
# 

# In[28]:


## TO-DO: Query 1:  Give me the artist, song title and song's length in the music app history that was heard during \
## sessionId = 338, and itemInSession = 4

session.execute("""
    CREATE TABLE IF NOT EXISTS session_songs
    (sessionId int, itemInSession int, artist text, song_title text, song_length float,
    PRIMARY KEY(sessionId, itemInSession))
    """)

                    


# In[29]:


file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) 
    for line in csvreader:
        query = "INSERT INTO session_songs (sessionId, itemInSession, artist, song_title, song_length)"
        query = query + " VALUES (%s, %s, %s, %s, %s)"
        artist_name, user_name, gender, itemInSession, user_last_name, length, level, location, sessionId, song, userId = line
        session.execute(query, (int(sessionId), int(itemInSession), artist_name, song, float(length)))


# #### Do a SELECT to verify that the data have been inserted into each table

# In[30]:


## TO-DO: Add in the SELECT statement to verify the data was entered into the table

rows = session.execute("""SELECT artist, song_title, song_length FROM session_songs WHERE sessionId = 338 AND itemInSession = 4""")

for row in rows:
    print(row.artist, row.song_title, row.song_length)


# ### COPY AND REPEAT THE ABOVE THREE CELLS FOR EACH OF THE THREE QUESTIONS

# In[31]:


## TO-DO: Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name)\
## for userid = 10, sessionid = 182

session.execute("""      

        create table if not exists event_log
            
            (artist text, 
            song text, 
            first_name text, 
            last_name text,
            user_id int,
            session_id int,
            item_in_session int, 
            primary key ((user_id, session_id), item_in_session))
""")                    


                    


# In[32]:


## TO-DO: Query 3: Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'

file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) 
    for line in csvreader:
        query = "INSERT INTO event_log (artist, song, first_name, last_name, user_id, session_id, item_in_session)"
        query = query + " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        session.execute(query, (line[0], line[9], line[1], line[4], int(line[10]), int(line[8]), int(line[3])))
                    


# In[33]:


# Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name)\
# for userid = 10, sessionid = 182
rows = session.execute("""
                            select artist , song , first_name , last_name
                            from event_log
                            where user_id = 10 and session_id = 182
                            order by item_in_session 

""")
for row in rows:
    print (row.artist , row.song , row.first_name , row.last_name)


# In[34]:


# Query 3: Give me every user name (first and last) in my music app history who listened to 
# the song 'All Hands Against His Own'
session.execute("""
                    create table if not exists song_users (
                    song text, user_id int, first_name text, last_name text, 
                    primary key (song, user_id))
""")


# In[35]:


file = 'event_datafile_new.csv'

df = pd.read_csv(file, usecols=[1, 4, 9, 10])
df.drop_duplicates(inplace=True)

for ix, row in df.iterrows():
    query = "INSERT INTO song_users (song, user_id, first_name, last_name)"
    query = query + " VALUES (%s, %s, %s, %s)"
    session.execute(query, (row['song'], row['userId'], row['firstName'], row['lastName']))


# In[36]:


rows = session.execute("""SELECT first_name, last_name FROM song_users WHERE song = 'All Hands Against His Own'""")

for row in rows:
    print( row.first_name, row.last_name )


# ### Drop the tables before closing out the sessions

# In[37]:


## TO-DO: Drop the table before closing out the sessions

session.execute("drop table session_songs")
session.execute("drop table event_log")
session.execute("drop table song_users")


# In[ ]:





# ### Close the session and cluster connection??

# In[19]:


session.shutdown()
cluster.shutdown()


# In[ ]:





# In[ ]:




