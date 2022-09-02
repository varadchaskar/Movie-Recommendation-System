# import pandas library
import pandas as pd

# Get the data
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
path = r"C:\Users\hp\Downloads\file.tsv"
df = pd.read_csv(path, sep='\t', names=column_names)

# Check out all the movies and their respective IDs
movie_titles = pd.read_csv(r"C:\Users\hp\Downloads\Movie_Id_Titles.csv")

data = pd.merge(df, movie_titles, on='item_id')

# creating dataframe with 'rating' count values
ratings = pd.DataFrame(data.groupby('title')['rating'].mean())

ratings['num of ratings'] = pd.DataFrame(data.groupby('title')['rating'].count())

ratings['num of ratings'].hist(bins = 70)

# Sorting values according to the 'num of rating column'
moviemat = data.pivot_table(index ='user_id',
			columns ='title', values ='rating')

ratings.sort_values('num of ratings', ascending = False).head(10)

# analysing correlation with similar movies
starwars_user_ratings = moviemat['Star Wars (1977)']

starwars_user_ratings.head()
# analysing correlation with similar movies
similar_to_starwars = moviemat.corrwith(starwars_user_ratings)

corr_starwars = pd.DataFrame(similar_to_starwars, columns =['Correlation'])
corr_starwars.dropna(inplace = True)

print(corr_starwars)

# Similar movies like starwars
corr_starwars.sort_values('Correlation', ascending = False).head(10)
corr_starwars = corr_starwars.join(ratings['num of ratings'])

corr_starwars.head()

print(corr_starwars[corr_starwars['num of ratings']>100].sort_values('Correlation', ascending = False))
