import csv

with open(r"C:\Users\hp\Downloads\Book1.csv", newline='') as f: #change this file directory
    reader = csv.reader(f)
    data = list(reader)

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

ist2=[]
for i in data:
    count=0
    ist=[]
    recommend=[]
    user_id=[]
    user_watched=[]
    for b in i:
        if count==0:
            print("user id:",b)
            user_id=b
            ist.append(user_id)
        if count%2 != 0 and count != 0:
            movie_name=b
            user_watched.append(movie_name)
            
        if count%2 == 0 and count != 0:
            user_rating=b
            
            if user_rating == 'null':
                user_rating=5
            if int(user_rating) >= 3:
                movie_name = movie_name
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
                        recommend.append(title_from_index)
                    if i==6:
                        break

            if int(user_rating) < 3:
                movie_name = movie_name
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
                        if title_from_index in recommend:
                            recommend.remove(title_from_index)
                    if i==4:
                        break
                        
        count +=1

    result = sorted(recommend, key = recommend.count, reverse = True)
    res = [i for n, i in enumerate(result) if i not in result[:n]]
    for i in res[:]:
        if i in user_watched:
            res.remove(i)
    count3=0
    for i in res:
        if count3<6:
            ist.append(i)
            count3+=1

    ist2.append(ist)

print(ist2)

fields = ['User id', 'Recomended movies'] 
    
    
# name of csv file 
filename = r"C:\Users\hp\Downloads\Book2.csv"

# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(ist2)

       



        

        

