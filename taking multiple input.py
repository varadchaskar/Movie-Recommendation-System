import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies_data = pd.read_csv(r"C:\Users\hp\Downloads\movies.csv")

selected_features = ['genres','keywords','tagline','cast','director']

for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)

ist=[]

while True:
    a=int(input("enter 1 for continue 2 for exit: "))
    if a==1:
        movie_name = input("enter a movie name")
        list_of_all_titles = movies_data['title'].tolist()
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 
        i = 0
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = movies_data[movies_data.index==index]['title'].values[0]
            i+=1
            if i>= 2:
                ist.append(title_from_index)
            if i==6:
                break
    if a==2:
        break

result = sorted(ist, key = ist.count, reverse = True)
print(ist)
print("now")
print(result)
print("after duplicate removing")
res = [i for n, i in enumerate(result) if i not in result[:n]]
 
print(res)