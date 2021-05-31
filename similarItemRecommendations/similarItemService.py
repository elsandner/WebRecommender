import ast

import pandas
from similarItemRecommendations import algorithmService


def searchMovies(title):
    try:
        print("Loading dataframe...")
        dataframeMovies = pandas.read_csv("archive/movies_metadata.csv", delimiter=',', low_memory=False)
    except Exception as e:
        print("Failed to load the dataset")
        print(e)
        return

    # filter metadata according to search title
    dataframeMovies = dataframeMovies[dataframeMovies['title'].str.contains(title, na=False)]

    return convertDfToDict(dataframeMovies)


def getSimilarMovies(movieId, algorithmId):

    similarMovies = applySimilarityAlgorithm(movieId, algorithmId) #List of Integers
    similarMoviesStr = map(str, similarMovies)

    try:
        print("Loading dataframe...")
        dataframeMovies = pandas.read_csv("archive/movies_metadata.csv", delimiter=',', low_memory=False)
    except Exception as e:
        print("Failed to load the dataset")
        print(e)
        return

    dataframeMovies = dataframeMovies[dataframeMovies['id'].isin(similarMoviesStr)]

    return convertDfToDict(dataframeMovies)

# helper Methods for searchMovies:
def reduce_genre_length(input_str): #input string "[{'id': 878, 'name': 'Science Fiction'}, {'id': 27, 'name': 'Horror'}]"
    result_list = []                  #output list   ['Science Fiction', 'Horror']
    data_dict_list = ast.literal_eval(input_str)
    for entry in data_dict_list:
        result_list.append(entry["name"])
    return result_list

# helper methods for getSimilarMovies:

def applySimilarityAlgorithm(movieId, algorithmId):

    # TODO: change algorithms as soon as they are implemented

    if algorithmId == 1:
        similarMovies = algorithmService.similarKeywords(movieId)
    elif algorithmId == 2:
        similarMovies = algorithmService.similarKeywords(movieId)
    elif algorithmId == 3:
        similarMovies = algorithmService.similarKeywords(movieId)
    elif algorithmId == 4:
        similarMovies = algorithmService.similarKeywords(movieId)
    elif algorithmId == 5:
        similarMovies = algorithmService.similarKeywords(movieId)
    else:
        similarMovies = ["invalid algorithmId"]

    return similarMovies


# general helpter methods:

# converts the movie metadata to a dict which only contains the needed data
# and is ready to be used for filling up the html template
def convertDfToDict(df: pandas.DataFrame):
    # remove unneeded columns from metadata df
    dataframeMovies = df[
        [
            "id",
            "title",
            "genres",
            "overview",
            "release_date",
            "vote_average",
            "vote_count"]
    ]

    # modify genres column from "[{'id': 18, 'name': 'Drama'}]" to "Drama" for better readability
    dataframeMovies["genres"] = dataframeMovies["genres"].apply(reduce_genre_length)

    # convert dataframe to dict, so the data can be used in the html easier
    return dataframeMovies.to_dict(orient="records")