import pandas as pd
movies = pd.read_csv("movies_metadata.csv", low_memory=False)
movie_actors = pd.read_csv("credits.csv", low_memory=False)

movie_actors['id'] = movie_actors['id'].apply(str)
merged = movies.set_index("id").join(movie_actors.set_index('id'))

# remove elements without title or cast
merged = merged[merged["title"].notnull()]
merged = merged[merged["cast"].notnull()]

# transform data
tf_genres = []
# tf_languages = []
# tf_companies = []
tf_cast = []
directors = []
for index, row in merged.iterrows():
    # genres
    tf_genres_row = []
    genres = eval(row["genres"])
    for genre in genres:
        tf_genres_row.append(genre["name"])
    tf_genres.append(tf_genres_row)

    #     # languages
    #     tf_languages_row = []
    #     languages = eval(row["spoken_languages"])
    #     for lan in languages:
    #         tf_languages_row.append(lan["name"])
    #     tf_languages.append(tf_languages_row)

    #     # companies
    #     tf_companies_row = []
    #     companies = eval(row["production_companies"])
    #     for com in companies:
    #         tf_companies_row.append(com["name"])
    #     tf_companies.append(tf_companies_row)

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
# merged["tf_languages"] = tf_languages
# merged["tf_companies"] = tf_companies
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
cols = ['title', 'tf_genres', 'tf_cast', 'director', 'release_date', 'vote_average', 'vote_count', 'revenue', 'runtime',
        'popularity']
merged = merged[cols]

# import keywords
keywords = pd.read_csv("keywords.csv")

# Keywords transformieren
tf_keywords = []

for index, row in keywords.iterrows():
    tf_row_keywords = []
    for key in eval(row["keywords"]):
        tf_row_keywords.append(key["name"])
    tf_keywords.append(tf_row_keywords)

keywords["tf_keywords"] = tf_keywords
del keywords["keywords"]

keywords['id'] = keywords['id'].apply(str)
merged = merged.join(keywords.set_index('id'))

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

from sklearn.feature_extraction.text import CountVectorizer

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(merged.head(2000)['summary'])

from sklearn.metrics.pairwise import cosine_similarity

cosine_sim = cosine_similarity(count_matrix, count_matrix)

merged = merged.reset_index()
indices = pd.Series(merged.index, index=merged['title'])

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """


    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return merged
