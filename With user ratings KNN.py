import pandas as pd
import numpy as np

movies_df=pd.read_csv(r"C:\Users\hp\Downloads\archive\movie.csv", usecols=['movieId','title'], dtype={'id':'int32','title':'str'})
movies_df.head()

ratings_df=pd.read_csv(r"C:\Users\hp\Downloads\ratings.csv",
    usecols=['userId', 'movieId', 'rating','timestamp'],dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})
ratings_df.head()

movies_df.isnull().sum()

ratings_df.isnull().sum()

print("Movies:",movies_df.shape)
print("Ratings:",ratings_df.shape)

movies_merged_df=movies_df.merge(ratings_df, on='movieId')
movies_merged_df.head()

movies_merged_df=movies_merged_df.dropna(axis = 0, subset = ['title'])
movies_merged_df.head()

movies_average_rating=movies_merged_df.groupby('title')['rating'].mean().sort_values(ascending=False).reset_index().rename(columns={'rating':'Average Rating'})
movies_average_rating.head()

movies_rating_count=movies_merged_df.groupby('title')['rating'].count().sort_values(ascending=True).reset_index().rename(columns={'rating':'Rating Count'}) #ascending=False
movies_rating_count_avg=movies_rating_count.merge(movies_average_rating, on='title')
movies_rating_count_avg.head()

rating_with_RatingCount = movies_merged_df.merge(movies_rating_count, left_on = 'title', right_on = 'title', how = 'left')
rating_with_RatingCount.head()

pd.set_option('display.float_format', lambda x: '%.3f' % x)
print(rating_with_RatingCount['Rating Count'].describe())

popularity_threshold = 50
popular_movies= rating_with_RatingCount[rating_with_RatingCount['Rating Count']>=popularity_threshold]
popular_movies.head()

movie_features_df=popular_movies.pivot_table(index='title',columns='userId',values='rating').fillna(0)
movie_features_df.head()

from scipy.sparse import csr_matrix
movie_features_df_matrix = csr_matrix(movie_features_df.values)

from sklearn.neighbors import NearestNeighbors
model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(movie_features_df_matrix)

indexNamesArr = movie_features_df.index.values
    
listOfRowIndexLabels = list(indexNamesArr)
name="Star Wars: Episode V - The Empire Strikes Back (1980)"
no=0
for i in range(len(listOfRowIndexLabels)):
    m_name=listOfRowIndexLabels[i]
    if m_name==name:
        no=i
        print(no)

query_index = no
distances, indices = model_knn.kneighbors(movie_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 6)

for i in range(0, len(distances.flatten())):

    if i == 0:
        print('Recommendations for {0}:\n'.format(movie_features_df.index[query_index]))
    else:
        print('{0}: {1}, with distance of {2}:'.format(i, movie_features_df.index[indices.flatten()[i]], distances.flatten()[i]))



