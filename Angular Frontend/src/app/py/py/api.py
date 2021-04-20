import flask
from flask import request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = flask.Flask(__name__)
app.config["DEBUG"] = True

movies = pd.read_csv('movies_metadata.csv', low_memory=False)
movie_actors = pd.read_csv("../movie_data/credits.csv", low_memory=False)
# join actors / crew and movie metadata on index
movie_actors['id'] = movie_actors['id'].apply(str)
merged = movies.set_index("id").join(movie_actors.set_index('id'))
# remove elements without title or cast
merged = merged[merged["title"].notnull()]
merged = merged[merged["cast"].notnull()]

# transform data
tf_genres = []
tf_cast = []
directors = []
for index, row in merged.iterrows():
    # genres
    tf_genres_row = []
    genres = eval(row["genres"])
    for genre in genres:
        tf_genres_row.append(genre["name"])
    tf_genres.append(tf_genres_row)

    # cast
    tf_cast_row = []
    casts = eval(row["cast"])
    for cast in casts:
        tf_cast_row.append(cast["name"])
    tf_cast.append(tf_cast_row)

    # director
    crew = eval(row["crew"])
    director = ""
    for person in crew:
        if person["job"] == "Director":
            director = person["name"]
            break
    directors.append(director)


# add data to table
merged["tf_genres"] = tf_genres
merged["tf_cast"] = tf_cast
merged["director"] = directors

# delete not used columns
col_dels = ["adult", "belongs_to_collection", "homepage", "imdb_id", "poster_path", "production_countries",
            "tagline", "video", "original_title", "status", "original_language", "overview", "budget", "genres",
            "spoken_languages", "production_companies", "cast", "crew"]
for col in col_dels:
    if col in merged.columns:
        del merged[col]

# change order of columns
cols = ['title', 'tf_genres', 'tf_cast', 'director', 'release_date',
        'vote_average', 'vote_count', 'revenue', 'runtime', 'popularity']
merged = merged[cols]

# import keywords
keywords = pd.read_csv("../movie_data/keywords.csv")

# Keywords transformieren
tf_keywords = []

for index, row in keywords.iterrows():
    tf_row_keywords = []
    for key in eval(row["keywords"]):
        tf_row_keywords.append(key["name"])
    tf_keywords.append(tf_row_keywords)

keywords["tf_keywords"] = tf_keywords
del keywords["keywords"]

# merge keywords and merged
keywords['id'] = keywords['id'].apply(str)
merged = merged.join(keywords.set_index('id'))

# namen konvertieren


def clean_names(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    elif isinstance(x, str):
        # director
        return str.lower(x.replace(" ", ""))


features = ['tf_cast', 'tf_keywords', 'director', 'tf_genres']

for feature in features:
    merged[feature] = merged[feature].apply(clean_names)


def create_summary(x):
    return ' '.join(x['tf_keywords']) + ' ' + ' '.join(x['tf_cast']) + ' ' + x['director'] + ' ' + ' '.join(x['tf_genres'])


merged["summary"] = merged.apply(create_summary, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(merged['summary'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)
merged = merged.reset_index()
indices = pd.Series(merged.index, index=merged['title'])

# Function that takes in movie title as input and outputs most similar movies


def get_recommendations(title, cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return merged['id'].iloc[movie_indices]


res = get_recommendations('Hounded', cosine_sim)
movies = []
for id in res:
    movies.append(merged[merged["id"] == id].values.tolist())
movies


@app.route('/', methods=['GET'])
def home():
    return {"test": movies}


@app.route('/all', methods=['GET'])
def getAllData():
    filtered = merged[["id", "title"]].values.tolist()
    return {"test": filtered}


@app.route('/getRecommendations', methods=['POST'])
def makeRecommendations():
    content = request.json
    print(content["ids"])
    recs = []
    for id in content["ids"]:
        print(id)
        try:
          res = get_recommendations(
            merged[merged["id"] == id]["title"].values[0], cosine_sim)
          recs.append([id, res.tolist()])
        except:
          print('fehler')

    return {"response": recs}



app.run()
