# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("movie_db.db")
cur = conn.cursor()

q1 = cur.execute("Select * from movie_data group by title")
movie = pd.DataFrame(data = q1.fetchall(),columns = ["Name","Year","Genre","Rating","Director","Star","Votes"])
print(movie)
print(movie.loc[0])
print(list(movie))


#rating and votes
x=movie.groupby('Rating')['Votes'].count()
df=pd.DataFrame(x)
df.index
plt.scatter(df.index,x,marker='*')
plt.xlabel('Rating')
plt.ylabel('No of votes')
plt.title('Rating vs Votes',fontsize=25)
plt.show()

#Top 3 movies
temp=movie.sort_values('Rating',ascending=False)
plt.bar(temp.iloc[0:3,0],temp.iloc[0:3,3],color='blue')
plt.xlabel('Name')
plt.ylabel('Rating')
plt.title('Top 3',fontsize=25)
plt.legend(['Value1','Value2'],loc=1)
plt.show()


#bottom 3
temp=movie.sort_values('Rating',ascending=True)
plt.bar(temp.iloc[0:3,0],temp.iloc[0:3,3],color='blue')
plt.xlabel('Name')
plt.ylabel('Rating')
plt.title('Bottom 3',fontsize=25)
plt.legend(['Value1','Value2'],loc=1)
plt.show()


#Year and votes
movie['Votes'] = movie['Votes'].astype('str')
movie['Votes'] = movie['Votes'].str.replace(',', '')
movie['Votes'] = pd.to_numeric(movie['Votes'], errors='coerce')
v=movie.sort_values('Votes',ascending=False)
v.iloc[0:5,[0,1,3,6]]
plt.bar(v.iloc[0:5,1],v.iloc[0:5,6],color='orange')
plt.xlabel('Year')
plt.ylabel('No of votes')
plt.title('Year vs Votes',fontsize=25)
plt.show()








