import ast

import pandas


class SimilarItemService:

    def searchMovies(self, title):
        try:
            print("Loading dataframe...")
            dataframeMovies = pandas.read_csv("archive/movies_metadata.csv", delimiter=',', low_memory=False)
        except Exception as e:
            print("Failed to load the dataset")
            print(e)
            return

        # filter metadata according to search title
        dataframeMovies = dataframeMovies[dataframeMovies['title'].str.contains(title, na=False)]

        # remove unneeded columns from metadata df
        dataframeMovies = dataframeMovies[
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
        searchMovies = dataframeMovies.to_dict(orient="records")

        return searchMovies


# helpter Methods:
def reduce_genre_length(input_str): #input string "[{'id': 878, 'name': 'Science Fiction'}, {'id': 27, 'name': 'Horror'}]"
    result_list = []                  #output list   ['Science Fiction', 'Horror']
    data_dict_list = ast.literal_eval(input_str)
    for entry in data_dict_list:
        result_list.append(entry["name"])
    return result_list
