# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Please Refer the Code Manual.

#Importing Library
import bs4
import requests
import sqlite3


#Connecting To SQl
conn = sqlite3.connect("movie_db.db")
cur = conn.cursor()

#cur.execute(' DROP TABLE IF exists movies_data') #Executes the query
#cur.execute('CREATE TABLE movie_data(title text,year integer,genre text,rating double,director text,star text,votes double)')  

#Connecting to Web-page through Beautiful Soup
url = "https://www.imdb.com/list/ls051231439/"
data = requests.get(url)
soup = bs4.BeautifulSoup(data.text,'html.parser')
res = soup.find_all('div',{'class':['lister-item-content']})
for r in res:
    title = r.find('a').text#Find to get the text
    year = r.find('span',{'class':'lister-item-year text-muted unbold'}).text
    genre = r.find('span','genre').text
    genre = genre.strip()
    rating = r.find('span','ipl-rating-star__rating').text
    votes = r.find('span',{'name':'nv'}).text
    crew = r.findAll('p',"text-muted text-small")[1]
    temp=[]
    x=crew.findAll('a')
    for i in range(0,len(x)):
        temp.append(crew.findAll('a')[i].get_text())
    stars = ','.join(temp[1:])
    #Inserting Values into SQL
    cur.execute("Insert into movie_data(title,year,genre,rating,director,star,votes) values(?,?,?,?,?,?,?)",(title,year,genre,rating,temp[0],stars,votes))
    conn.commit()   
 
#Database Created
    

    


    
    
    
    
    
    
    