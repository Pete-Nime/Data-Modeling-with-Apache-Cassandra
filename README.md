## Data-Modeling-with-Apache-Cassandra

## Table of Content 

 - Datasets
The project is based  one dataset: event_data. The directory of CSV files partitioned by date. Here are examples of filepaths to two files in the dataset:

event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv

- Prject include Jupyer notebook process the event_datafile_new.csv.

- Modeling of NoSQL database or Apache Cassandra database

## Introductions

The Sparkigy music app company request help with to analyse the the trend of users on their app. Since the consumer increase in listening to their 
favorite songs and adability to the music app. They want a data engineer to extract the uses information stored on the csv_file format on the user 
activity. Thus the number of users are also incread since the last time when useer information were stored on PostgreSQL database. Now the data engineer
will apply Apachi Cassandra to retrieve data on the csv_file format. This will help sparkify analyst to employ query of the set data for the desire
output to meet their business objectives. 



## Executive Summary

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

thus they want hire a data engineer to create an Apache Cassandra database which can create queries on song play data to answer the questions, and wish to bring you on the project. The role is to create a database for this analysis. As a data engineer you will be able to test your database by running queries given to you by the analytics team from Sparkify to create the results.




## How to Install & Run the Project

- Design tables to answer the queries outlined in the project template

- Write Apache Cassandra CREATE KEYSPACE and SET KEYSPACE statements

- Develop the CREATE statement for each of the tables to address each question

- Load the data with INSERT statement for each of the tables

Include IF NOT EXISTS clauses in the CREATE statements to create tables only if the tables do not already exist. Also include DROP TABLE statement for each table, this way you can run drop and create tables whenever you want to reset your database and test your ETL pipeline
Test by running the proper select statements with the correct WHERE clause

## Files & Questions to be worked with are as follows

![image](https://user-images.githubusercontent.com/103359089/210189861-1a47567b-7754-4fc1-b15a-629e2a9cf0e9.png)

- Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4

- Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182

- Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'



