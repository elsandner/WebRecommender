import ast

import numpy
import pandas
from numpy import ndarray
from pandas import DataFrame

def similarity(dataframeMovies:DataFrame, genreList: list)->float:
    # compute similarity according to the slide 2 page 7
    intersec = set(dataframeMovies["genres"]).intersection(set(genreList))
    simi = (2 * len(intersec)) / (len(dataframeMovies["genres"]) + len(genreList))
    return simi

def wighted_similarity(dataframeMovies:DataFrame, genreList: dict) -> float:
    # compute similarity according to TF_IDF
    simi = 0
    for genre in dataframeMovies["genres"]:
        for key, value in genreList.items():
            if str(genre) == str(key):
                simi += value
    return simi

def TF_IDF(genreList: dict, dataframeMovies)->float:
    # compute TF_IDF according to the slide 2 page 9
    TF_IDF_dict = {}
    summ = sum(list(genreList.values()))
    # dataframeMovies = dataframeMovies.head(1000)
    for key, value in genreList.items():
        mask = dataframeMovies["genres"].apply(lambda x: any(item for item in [key] if item in x))
        new_dataframeMovie = dataframeMovies[mask]
        TF_IDF_dict[key] = (value/summ)*numpy.log(len(dataframeMovies)/len(new_dataframeMovie))
    print(TF_IDF_dict)
    return TF_IDF_dict

def countRatings(dataframeMovies: DataFrame, dataframeRatings:DataFrame):
    # counting the numbers of ratings for each movies
    count = 0
    dataframeRatings['movieId'] = dataframeRatings['movieId'].astype(str)
    for _,d in dataframeRatings.head(10000).iterrows():
        if d["movieId"] == dataframeMovies["id"]:
            count += 1
    return count

# determine the popularity of any item by counting the numbers of ratings for it.
def computePopularity(dataframeMovies: DataFrame, dataframeRatings:DataFrame):
    print("\n\n--------- TASK computePopularity -----------")
    print("Number of the overlapped movie: ", len(dataframeMovies))
    dataframeMovies["countRatings"] = dataframeMovies.apply(lambda x: countRatings(x,dataframeRatings), axis=1)
    dataframeMovies = dataframeMovies.sort_values(by="countRatings", ascending=False)
    return dataframeMovies


def reduce_genre_length(input_str: str) -> list:
    """Reduces the length of a string i.e: \n
     [{'id': 878, 'name': 'Science Fiction'}, ... ] to ["Science Fiction", ...] """
    result_list=[]
    data_dict_list = ast.literal_eval(input_str)
    for entry in data_dict_list:
        result_list.append(entry["name"])
    return result_list


def cleanId(id):
    # print(dataframeMovies)
    try:
        return int(id)

    except:
        return -1