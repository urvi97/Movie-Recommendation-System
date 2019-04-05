# -*- coding: utf-8 -*-

#Please Refer the Code Manual

#Importing the Libraries
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#Connecting to Database
conn = sqlite3.connect("movie_db.db")
cur = conn.cursor()


#Converting It into DataFrames
q1 = cur.execute("Select * from movie_data group by title")
df = pd.DataFrame(data = q1.fetchall(),columns = ["Name","Year","Genre","Rating","Director","Star","Votes"])
print(df)
print(type(df))

#CLosing the Connection
conn.close()

#Recommendation on the Based of Popularity

#Loading the Data
movie_data = df
#Viewing The Data
print(movie_data.head())

print(list(movie_data))

print(movie_data.shape)

print(sum(movie_data.isnull().values))

#Calculating the mean of rating
avg_rating = movie_data['Rating'].mean()
print(avg_rating)
#We can see the average Rating is 6.8 out of 10

#Converting the type of Votes
print(movie_data.dtypes)
movie_data['Votes'] = movie_data['Votes'].astype('str')
movie_data['Votes'] = movie_data['Votes'].str.replace(',', '')
movie_data['Votes'] = pd.to_numeric(movie_data['Votes'], errors='coerce')
print(movie_data.dtypes)

#Calculating Minimum Number of votes to be considered
min_votes = movie_data['Votes'].quantile(0.70)
print(min_votes)
#We can say that min required votes are 39521.5

#Filtering out the movies with Min votes
movies= movie_data.loc[movie_data['Votes'] >= min_votes]
movies.shape

#Now On basis of above information we can calculate are score metric
def weighted_rating(x,m = min_votes,c= avg_rating):
    V = x['Votes']
    R = x['Rating']
    return (((V/V+m)*R) + ((m/V+m)*c))

movies['score'] = movies.apply(weighted_rating, axis=1)

#Viewing top ten movies/Series
movies = movies.sort_values('score',ascending=False)
movies[['Name','score']].head(10)


#Content Based Recommendation

movie = df

#Removing the lowercase and strip all the spaces between them
def clean_data(x):
	#print(x)
	#print(type(x))
	temp=str.lower(x.replace(" ",""))
	return temp

feature = ['Genre','Director','Star']

for f in feature:
	movie[f]= movie[f].apply(clean_data)

def clean_data1(x):
	#print(x)
	#print(type(x))
	temp=str.lower(x.replace(","," "))
	return temp

movie['Star']= movie['Star'].apply(clean_data1)

#create  "soup", which is a string that contains all the data that you want to feed to your
#vectorizer (namely actors, director and genre).
def create_soup(x):
    return x['Star'] + ' ' + x['Director'] + ' ' + x['Genre']

movie['soup'] = movie.apply(create_soup, axis=1)

#Convert a collection of text documents to a matrix of token counts
count = CountVectorizer()
count_matrix = count.fit_transform(movie['soup'])

#finding cosine similarity
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

#Construct a map of indices and movie titles
indices = pd.Series(movie.index, index=movie['Name'])


# Function that takes in movie title as input and outputs most similar movies

def recommend(name):
	#Get index of the movie wrt to the name called
	indx=indices[name]

	#get the pariwise similarity scores of all the movies wrt the movie called
	#enumerate used so that we can assin a number to each similar movie
	similar_score = list(enumerate(cosine_sim2[indx]))
	print(similar_score)

	#sort the movie based on the similarity score as we want top 10 similar movies
	similar_score=sorted(similar_score,key=lambda x:x[1],reverse=True)
	#print(sim_score)

	sim_score = list(similar_score[1:11])
	print(sim_score)

	mvi_lst=[]
	for i in sim_score:
		mvi_lst.append(movie['Name'].iloc[i[0]])
		#print(mvi_lst)
	return mvi_lst

recommend('1921')
def get_mvi_details(inp):
    
    indices1 = pd.Series(movie_data.index, index=movie_data['Name'])
    #dic={'name':'xyx','Genre':'acb','Actors':'act','Director':'dir'}
    nm="Name:" + movie_data['Name'].loc[indices1[inp]]
    gn="Genre:" + movie_data['Genre'].loc[indices1[inp]]
    der="Director:" + movie_data['Director'].loc[indices1[inp]]
    st="Star:" + movie_data['Star'].loc[indices1[inp]]
    #dic.update({'name':nm,'Genre':gn,'Actors':st,'Director':der})
    #df=pd.DataFrame(dic)
    return [nm,gn,der,st]


#Deployment

#Importing Library
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Boostrap CSS.


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})
colors = {
    'background': '#E0FFFF',
    'text': '#8B008B'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Movie World',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
     html.Div(html.H3(children='Search Your Movie', style={
        'textAlign': 'left',
        'color': colors['text'],
        }
     )),
     html.Div([
    dcc.Input(id='my-id', value='1921', type='text'),
    html.Div(id='my-div',style={'backgroundColor': colors['background'],'color' : '#4B0082','font-family':'Times Roman','font-size':'100%',"font-weight":"bold"}),
    html.Div(id='my-div1',style={'backgroundColor': colors['background'],'color':'Black','font-family':'verdana','font-size':'100%',"font-weight":"bold"}),
],className ='three columns'),

    html.Div(html.H2(children='Upcoming Movies', style={
        'textAlign': 'center',
        'color': colors['text'],
        }
     )),
     html.Div([
             html.A([ 
            html.Img(
                src='https://m.media-amazon.com/images/M/MV5BY2MwM2ZhNTItMzkwNi00MTQxLTljMDAtZTk1YmU2M2YzNGVmXkEyXkFqcGdeQXVyNjE1OTQ0NjA@._V1_UY268_CR2,0,182,268_AL_.jpg',
                style={
                    'height' : 300,
                    'width' : 200,
                    'float' : 'middle',

                    'position' : 'center',
                    'padding-top' : 0,
                    'padding-right' : 0,
					'backgroundColor': 'red'

                }),] ,href='https://www.youtube.com/watch?v=-JLewvWBkCw&t=29s'),
                 html.A([ 
                html.Img(
                    src='https://upload.wikimedia.org/wikipedia/en/thumb/0/07/Gully_Boy_poster.jpg/220px-Gully_Boy_poster.jpg',
                    style={
                        'height' : 300,
                        'width' : 200,
                        'float' : 'middle',

                        'position' : 'center',
                        'padding-top' : 0,
                        'padding-right' : 0,
    					'backgroundColor': 'red'

                    }
                    ),] ,href='https://www.youtube.com/watch?v=S4juMK7WGvc'),
            html.A([ 
            html.Img(
                    src='https://m.media-amazon.com/images/M/MV5BMTdiN2Q2MGUtYWRjMi00M2Y2LWEzOTYtOTA3NjNiMGMzNmFhXkEyXkFqcGdeQXVyNjE1OTQ0NjA@._V1_UY268_CR4,0,182,268_AL_.jpg',
                    style={
                        'height' : 300,
                        'width' : 200,
                        'float' : 'middle',

                        'position' : 'center',
                        'padding-top' : 0,
                        'padding-right' : 0,
    					'backgroundColor': 'red'

                    }
                    ),] ,href='https://www.youtube.com/watch?v=fo9EhcwQXcM'),
            html.A([ 
            html.Img(
                    src='https://m.media-amazon.com/images/M/MV5BZGE1NGYxOWItODdmMy00NWNhLTgxZmMtYmVjYmViMGI0NTdmXkEyXkFqcGdeQXVyNzE2MTQyMzM@._V1_UY1200_CR90,0,630,1200_AL_.jpg',
                    style={
                        'height' : 300,
                        'width' : 200,
                        'float' : 'middle',

                        'position' : 'center',
                        'padding-top' : 0,
                        'padding-right' : 0,
    					'backgroundColor': 'red'

                    }
                    ),] ,href='https://www.youtube.com/watch?v=8ZwgoVmILQU'),
              html.A([
             html.Img(
                    src='https://timesofindia.indiatimes.com/thumb/62379872.cms?width=219&height=317&imgsize=78725',
                    style={
                        'height' : 300,
                        'width' : 200,
                        'float' : 'middle',

                        'position' : 'center',
                        'padding-top' : 0,
                        'padding-right' : 0,
    					'backgroundColor': 'red'

                    }
                    ),] ,href='https://www.youtube.com/watch?v=Ez5W8SN9Bqc'),
     html.H3(children='Popular Movies', style={
        'textAlign': 'center',
        'color': colors['text'],

        }),
        dcc.Graph(
        id='Popular_Movies',
        figure={
            'data': [
                {'x': movies['Name'].head(10), 'y': movies['score'].head(10), 'type': 'bar', 'name': 'SF'},
                #{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'height': 355,
                'width':1030,
                'padding-top' :0,
                'font': {
                    'color': colors['text']
                }
            }
        },className ='two columns'
    )]),
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)

def update_output_div(input_value):
    trial = get_mvi_details(input_value)
    return  html.Table (
            [html.Tr(html.Td(col)) for col in trial])

@app.callback(
    Output(component_id='my-div1', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)

def update_output_act(input_value):
    trial = recommend(input_value)
    #df=pd.DataFrame(trial,columns='Movies')
    return html.Table (
           [html.Tr("Movies you may like")] +
            [html.Tr(html.Td(col)) for col in trial])

if __name__ == '__main__':
    app.run_server(debug=True)
