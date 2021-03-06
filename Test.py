from similarItemRecommendations import algorithmService, similarItemService

def testSimilarGenres():
    movieId = 862
    df = similarItemService.loadDF("archive/movies_metadata.csv")
    result = algorithmService.similarGenres(movieId, df)
    print(result)

def testmMviesByDirectors():
    movieId = 862
    df = similarItemService.loadDF("archive/movies_metadata.csv")
    result = algorithmService.similarDirectors(movieId, df)
    print(result)

def main():
    # testSimilarGenres()
    testmMviesByDirectors()

main()