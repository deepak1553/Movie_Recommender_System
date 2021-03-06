# -*- coding: utf-8

# PROBLEM STATEMENT

- This notebook implements a movie recommender system. 
- Recommender systems are used to suggest movies or songs to users based on their interest or usage history. 
- For example, Netflix recommends movies to watch based on the previous movies you've watched.  
- In this example, we will use Item-based Collaborative Filter 



- Dataset MovieLens: https://grouplens.org/datasets/movielens/100k/ 
- Photo Credit: https://pxhere.com/en/photo/1588369

![image.png](attachment:image.png)

# STEP #0: LIBRARIES IMPORT
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

"""# STEP #1: IMPORT DATASET"""

# Two datasets are available, let's load the first one:
movie_titles_df = pd.read_csv("Movie_Id_Titles")
movie_titles_df.head(20)

# Let's load the second one!
movies_rating_df = pd.read_csv('u.data', sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])

movies_rating_df.head(10)

movies_rating_df.tail()

# Let's drop the timestamp 
movies_rating_df.drop(['timestamp'], axis = 1, inplace = True)

movies_rating_df

movies_rating_df.describe()

movies_rating_df.info()

# Let's merge both dataframes together so we can have ID with the movie name
movies_rating_df = pd.merge(movies_rating_df, movie_titles_df, on = 'item_id')

movies_rating_df

movies_rating_df.shape

"""# STEP #2: VISUALIZE DATASET"""

movies_rating_df.groupby('title')['rating'].describe()

ratings_df_mean = movies_rating_df.groupby('title')['rating'].describe()['mean']

ratings_df_count = movies_rating_df.groupby('title')['rating'].describe()['count']

ratings_df_count

ratings_mean_count_df = pd.concat([ratings_df_count, ratings_df_mean], axis = 1)

ratings_mean_count_df.reset_index()

ratings_mean_count_df['mean'].plot(bins=100, kind='hist', color = 'r')

ratings_mean_count_df['count'].plot(bins=100, kind='hist', color = 'r')

# Let's see the highest rated movies!
# Apparently these movies does not have many reviews (i.e.: small number of ratings)
ratings_mean_count_df[ratings_mean_count_df['mean'] == 5]

# List all the movies that are most rated
# Please note that they are not necessarily have the highest rating (mean)
ratings_mean_count_df.sort_values('count', ascending = False).head(100)

"""# STEP #3: PERFORM ITEM-BASED COLLABORATIVE FILTERING ON ONE MOVIE SAMPLE"""

userid_movietitle_matrix = movies_rating_df.pivot_table(index = 'user_id', columns = 'title', values = 'rating')

userid_movietitle_matrix

titanic = userid_movietitle_matrix['Titanic (1997)']

titanic

# Let's calculate the correlations
titanic_correlations = pd.DataFrame(userid_movietitle_matrix.corrwith(titanic), columns=['Correlation'])
titanic_correlations = titanic_correlations.join(ratings_mean_count_df['count'])

titanic_correlations

titanic_correlations.dropna(inplace=True)
titanic_correlations

# Let's sort the correlations vector
titanic_correlations.sort_values('Correlation', ascending=False)

titanic_correlations[titanic_correlations['count']>80].sort_values('Correlation',ascending=False).head()

# Pick up star wars movie and repeat the excerise

"""# STEP#4: CREATE AN ITEM-BASED COLLABORATIVE FILTER ON THE ENTIRE DATASET """

# Recall this matrix that we created earlier of all movies and their user ID/ratings
userid_movietitle_matrix

movie_correlations = userid_movietitle_matrix.corr(method = 'pearson', min_periods = 80)
# pearson : standard correlation coefficient
# Obtain the correlations between all movies in the dataframe

movie_correlations

# Let's create our own dataframe with our own ratings!
myRatings = pd.read_csv("My_Ratings.csv")
#myRatings.reset_index

myRatings

len(myRatings.index)

myRatings['Movie Name'][0]

similar_movies_list = pd.Series()
for i in range(0, 2):
    similar_movie = movie_correlations[myRatings['Movie Name'][i]].dropna() # Get same movies with same ratings
    similar_movie = similar_movie.map(lambda x: x * myRatings['Ratings'][i]) # Scale the similarity by your given ratings
    similar_movies_list = similar_movies_list.append(similar_movie)

similar_movies_list.sort_values(inplace = True, ascending = False)
print (similar_movies_list.head(10))
