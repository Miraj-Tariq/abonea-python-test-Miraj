import logging

from backend import movie
from backend.constants import base_setup_count, omdb_base_url, title_word
from backend.utils.api_helper import custom_request


OMDB_KEY = '5d311330'


class OMDBMoviesBaseSetup:
    """
    A class to initialize and populate movies in the database using the OMDB API.

    Args:
        search_word (str, optional): The search term to use when querying the OMDB API. Defaults to title_word.
        count (int, optional): The number of movies to insert into the database. Defaults to base_setup_count.
    """

    def __init__(self, search_word=title_word, count=base_setup_count):
        """
        Initializes a new instance of the OMDBMoviesBaseSetup class.

        Args:
            search_word (str, optional): The search term to use when querying the OMDB API. Defaults to title_word.
            count (int, optional): The number of movies to insert into the database. Defaults to base_setup_count.

        Returns:
            None

        """
        # Get the OMDB API key from the environment variables
        api_key = OMDB_KEY

        # Initialize variables for tracking the number of movies and the current page number
        movies_count, page = 0, 1

        # Loop through pages of search results until the desired number of movies has been inserted into the database
        while movies_count < count:
            # Make a request to the OMDB API to get a page of search results
            data = custom_request(
                omdb_base_url,
                s=search_word,
                page=page,
                apikey=api_key
            )
            # Check if the response was successful
            if data["Response"] == "True":
                # Extract the movies from the search results
                movies = data["Search"]

                # Loop through each movie in the search results
                for movie in movies:
                    # Only insert movies that have a type of "movie"
                    if movie["Type"] == "movie":
                        # Insert the movie into the database
                        self.insert_movie(movie)
                        movies_count += 1

                        # If the desired number of movies has been inserted into the database, break out of the loop
                        if movies_count >= count:
                            break
            else:
                # If the search returns no more results, log a message and break out of the loop
                logging.info("All movies against search word {} has been extracted. "
                             "Total movies inserted in DB are {}".format(search_word, movies_count))
                break

            # Increment the page number and repeat the loop for the next page of search results
            page += 1

    @staticmethod
    def insert_movie(movie_data):
        """
        Inserts a single movie into the database.

        Args:
            movie_data (dict): A dictionary containing the movie data to insert into the database.

        Returns:
            None

        """
        if "imdbID" in movie_data and movie_data["imdbID"]:
            return movie.Movie.create(
                movie_data["imdbID"],
                movie_data["Type"] if "Type" in movie_data and movie_data["Type"] else "movie",
                movie_data["Title"] if "Title" in movie_data and movie_data["Title"] else "No Title",
                movie_data["Year"] if "Year" in movie_data and movie_data["Year"] else "0000",
                movie_data["Poster"] if "Poster" in movie_data and movie_data["Poster"] else ""
            )
