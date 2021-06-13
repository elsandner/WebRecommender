import pandas
from similarItemRecommendations import util, similarItemService
from ast import literal_eval
import numpy as np

def calcSimilarity(kw1: pandas.Series, kw2: pandas.Series):   # kw..keyword list

    kw1_length = len(kw1)
    kw2_length = len(kw2)

    kw_intersection = list(set(kw1) & set(kw2))
    kw_intersection_length = len(kw_intersection)

    similarity = 2 * kw_intersection_length / (kw1_length + kw2_length)
    return similarity


# Algorithm 1 of 5
# Compares the similarity of the movies keyword and all other movies keywords to find most similar movies
# returns list of 5 most similar movies
def similarKeywords(movieId: int, keywords_DF):

    try:
        movieId = int(movieId)
    except ValueError:
        return False
    print(keywords_DF[keywords_DF["id"] == movieId])
    mainKW_String = keywords_DF[keywords_DF["id"] == movieId].iloc[0]['keywords']
    keywords_DF = keywords_DF[keywords_DF["id"] != movieId]  # remove main-keywords from keywords_DF

    # change separator between dicts to avoid splitting on ', ' in dict
    mainKW_String = mainKW_String.replace('}, ', '}|')

    mainKW_List = mainKW_String.strip('][').split('|')

    similarity_dict = {}
    for index, movie in keywords_DF.iterrows():
        kw2Series = pandas.Series(movie["keywords"])

        kw2String = kw2Series.get(0)
        kw2String = kw2String.replace('}, ', '}|')

        kw2List = kw2String.strip('][').split('|')

        similarity = calcSimilarity(mainKW_List, kw2List)
        similarity_dict[movie["id"]] = similarity

    # sort similarity_dict by decreasing values
    similarity_dict_sorted = sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True)
    similarity_dict_sorted = similarity_dict_sorted[:5]
    bestMovies = []

    for element in similarity_dict_sorted:
        bestMovies.append(element[0])

    print("5 most similar movies to ", movieId, ":\n ", similarity_dict_sorted)
    return bestMovies

# Algorithm 2 of 5
# Compares the similarity of the movies genres and all other movies genres to find most similar movies
# returns list of 5 most similar movies
def similarGenres(movieId: int, dataframeMovies):
    try:
        movieId = int(movieId)
    except ValueError:
        return False
    df = dataframeMovies[dataframeMovies["id"] == str(movieId)]
    df = df[["id", "title", "genres"]]
    df["genres"] = df["genres"].apply(util.reduce_genre_length)
    gernres = (df.iloc[0]["genres"])
    print(gernres)
    movies_df = dataframeMovies[["id", "title", "genres"]]
    movies_df["genres"] = movies_df["genres"].apply(util.reduce_genre_length)
    movies_df["similarity"] = movies_df.apply(lambda x: util.similarity(x, gernres), axis=1)
    genres_dict = {}
    for genre in gernres:
        genres_dict[genre] = 1
    TF_IDF_value = util.TF_IDF(genres_dict, dataframeMovies)
    movies_df["similarity"] = movies_df.apply(lambda x: util.wighted_similarity(x, TF_IDF_value), axis=1)
    movies_df = movies_df.sort_values(by="similarity", ascending=False)
    movies_df = movies_df[movies_df.id !=  str(movieId)]
    print(movies_df.head(5))
    return movies_df.head(5)["id"].tolist()

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan


# Algorithm 3 of 5
# Compares the similarity of the movies' directors and all other movies movies' directors to find most similar movies
# returns list of 5 most similar movies
def similarDirectors(movieId: int, dataframeMovies):
    try:
        movieId = int(movieId)
    except ValueError:
        return False
    # Load keywords and credits
    df = dataframeMovies[dataframeMovies["id"] == str(movieId)]
    df = df[["id", "title", "genres"]]
    df["genres"] = df["genres"].apply(util.reduce_genre_length)
    gernres = (df.iloc[0]["genres"])
    genres_dict = {}
    for genre in gernres:
        genres_dict[genre] = 1
    TF_IDF_value = util.TF_IDF(genres_dict, dataframeMovies)

    credits = similarItemService.loadDF("archive/credits.csv")
    movies_df = dataframeMovies[['id', 'title', 'genres']]
    movies_df["genres"] = movies_df["genres"].apply(util.reduce_genre_length)
    # # Remove rows with bad IDs.
    credits["id"] = credits["id"].apply(util.cleanId)
    credits= credits[credits.id != -1]
    movies_df["id"] = movies_df["id"].apply(util.cleanId)
    credits = credits[credits.id != -1]

    selectedCredit = credits[credits["id"] == int(movieId)]
    selectedCredit['crew'] = selectedCredit['crew'].apply(literal_eval)
    selectedCredit['director'] = selectedCredit['crew'].apply(get_director)
    selectedDirector = selectedCredit.iloc[0]["director"]

    # Merge keywords and credits into your main metadata dataframe
    metadata = movies_df.merge(credits, on='id')
    metadata = metadata[['id', 'title', 'genres', 'crew']]
    metadata['crew'] = metadata['crew'].apply(literal_eval)
    metadata['director'] = metadata['crew'].apply(get_director)
    metadata = metadata[['id', 'title', 'genres', 'director']]

    metadata["similarity"] = metadata.apply(lambda x: util.wighted_similarity(x, TF_IDF_value), axis=1)
    metadata = metadata.sort_values(by="similarity", ascending=False)
    metadata = metadata[metadata.id !=  str(movieId)]
    metadata = metadata[metadata["director"] == selectedDirector]
    print(metadata.head(5))
    return metadata.head(5)["id"].tolist()

