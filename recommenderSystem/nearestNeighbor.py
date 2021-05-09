from numpy import ndarray
import pandas
from pandas.core.frame import DataFrame
import ast


# This file is a copy of assignment 3
class NearestNeighbor:

    #TODO: i guess __init__ is not needed and this file does not need to be a class
    def __init__(self):
        try:
            print("Loading dataframes...")
            # Loading this here, because it takes some time and will be used both in task A and B   !?!??! And C?
            self.dataframeRatings = pandas.read_csv("../archive/ratings_small.csv", delimiter=',',            # self .. this is a class variable
                                               low_memory=False)
            self.dataframeMovies = pandas.read_csv("../archive/movies_metadata.csv", delimiter=',',
                                              low_memory=False)

        except Exception as e:
            print("Failed to load the dataset")
            print(e)
            return

    def validateUserId(self, userId) -> bool:
        try:
            userId = int(userId)
        except ValueError:
            return False

        try:
            # Loading this here, because it takes some time and will be used both in task A and B   !?!??! And C?
            dataframeRatings = pandas.read_csv("archive/ratings_small.csv", delimiter=',',            # self .. this is a class variable
                                               low_memory=False)
        except Exception as e:
            print("Failed to load the dataset")
            print(e)
            return

        result = int(userId) in dataframeRatings["userId"].unique()
        return result

    def getRecommendation(self, userId):    # like main in assignment3
        try:
            print("Loading dataframes...")
            dataframeRatings = pandas.read_csv("archive/ratings_small.csv", delimiter=',',
                                               low_memory=False)  # low_memory=False was suggested by PyCharm to get rid off DTypeWarning
            dataframeMovies = pandas.read_csv("archive/movies_metadata.csv", delimiter=',',
                                              low_memory=False)
        except Exception as e:
            print("Failed to load the dataset")
            print(e)
            return

        try:
            userId = int(userId)
        except ValueError:
            return False

        rated_movies = task_3B(dataframeRatings, dataframeMovies, userId)
        topMovies = task_3C(rated_movies, dataframeMovies)

        topMovies["genres"] = topMovies["genres"].apply(reduce_genre_length)

        return topMovies

# end of class - code below is basically a copy of assignment 3



# -------- TASK 2 --------------#

def task_3B(dataframeRatings, dataframeMovies, user_id):
    """Task 3 B) Shows the titles and genres of up to 15 movies that this user has rated """
    print("\n\n--------- TASK B) -----------")

    # Since we only need the subset of the ratings for that specific user, the whole dataframe is not required
    dataframeRatingsSubset = dataframeRatings[dataframeRatings["userId"] == user_id]
    # print(dataframeRatingsSubset)

    # The id in dataframeRatings is int64, but in dataframeMovies it is a string.
    # This results in an error when merging, because it tries to merge 2 columns of different types.
    # Solution: Convert the movieId from int64 to str
    dataframeRatings['movieId'] = dataframeRatingsSubset['movieId'].astype(str)

    dataframeMerged = dataframeMovies.merge(dataframeRatings, how='inner', left_on='id', right_on='movieId').head(15)

    # modify genres column from "[{'id': 18, 'name': 'Drama'}]" to "Drama" for better readability
    dataframeMerged["genres"] = dataframeMerged["genres"].apply(reduce_genre_length)

    # They are merged based on the movie id.
    # Since we want to get movies that a user has rated, it doesn't make sense
    print("\nMovies User " + str(user_id) + " has rated: ")
    print(dataframeMerged[["title", "genres",
                           "rating"]])  # Rating is not required in the task B) description, but it would be usefull in task C)
    return dataframeMerged[["title", "genres", "rating"]]


# -------- TASK 3 --------------#

def task_3C(rated_movies, dataframeMovies):

    sampled_movies = dataframeMovies[
        ["id",      # TODO: remove unneeded columns
         "title",
         "genres",
         "overview",
         "release_date",
         "vote_average",
         "vote_count"]
        ].sample(frac=0.10, random_state=1)

    # modify genres column from "[{'id': 18, 'name': 'Drama'}]" to "Drama" for better readability
    sampled_movies["genres"] = sampled_movies["genres"].apply(reduce_genre_length)

    # print(sampled_movies)
    k = 20  # Neighbours to consider
    movie_score_dict = calculate_score(rated_movies, sampled_movies, k)
    topMovies = dict(list(movie_score_dict.items())[0: 20])  # get first 20 Movies

    metaData = dataframeMovies[dataframeMovies['id'].isin(topMovies.keys())]
    metaData = metaData
    return metaData[["id", "title", "genres", "overview", "release_date", "vote_average", "vote_count"]]


# Helper Methods for getRecommendations
def reduce_genre_length(input_str): #input string "[{'id': 878, 'name': 'Science Fiction'}, {'id': 27, 'name': 'Horror'}]"
    result_list = []                  #output list   ['Science Fiction', 'Horror']
    data_dict_list = ast.literal_eval(input_str)
    for entry in data_dict_list:
        result_list.append(entry["name"])
    return result_list


def calculate_score(rated_movies, sampled_movies, k):
    print("Calculating scores...")
    count = 0   # used just for printing progress
    movie_score_dict = dict()
    for index, new_movie in sampled_movies.iterrows():
        movie_score_dict[new_movie["id"]] = kNN(rated_movies, new_movie, k)    # check only the first k movies
        count += 1
        if count % 1000 == 0:
            print("Calculated " + str(count) + " scores")

    # sort movie_score_dict
    movie_score_dict = {k: v for k, v in sorted(movie_score_dict.items(), reverse=True, key=lambda item: item[1])}
    print("Calculated total of " + str(count) + " scores")
    return movie_score_dict


def kNN(rated_movies, new_movie, k):
    """ Calculates the distance between all rated movies and a new movie """
    score_list = []
    for index, rated_row in rated_movies.iterrows():
        dist = calculate_distance(rated_row["genres"], new_movie["genres"])
        score_list.append((1-dist)*float(rated_row["rating"]))

    #calculez disntantele, aleg filemele cu cele mai mici k distante
    #score = avg ((1-dist1) * rating1 , (1-dist2)*rating2, ...)

    score_list.sort(reverse=True)   # Sort in decreasing order
    score_list = score_list[:k]     # The highest k elements
    final_score = float(sum(score_list)/len(score_list)) # get the average of the first k elements (because we sorted them in decreasing order, htey have the highest score)
    return final_score


def calculate_distance(list1, list2) -> float:
    common_elements = set(list1).intersection(list2)
    list1.extend(list2)
    total_elements = set(list1)

    return float(1 - float(len(common_elements) / len(total_elements)))




# TODO's:
    # only load dataframes once
    # show something like "calculating recommendations .. "
    # cleanup code (I guess there are is some unneeded stuff ..)
    # define param and return datatypes
