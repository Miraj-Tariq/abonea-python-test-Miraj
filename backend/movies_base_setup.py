from backend.constants import omdb_base_url, title_word, base_setup_count
from backend.utils import request
from backend import movie

import logging
import os
from dotenv import load_dotenv

load_dotenv()


class OMDBMoviesBaseSetup:
    def __init__(self, search_word=title_word, count=base_setup_count):
        api_key = os.getenv("OMDB_KEY")
        movies_count, page = 0, 1
        page = 1
        while movies_count < count:
            data = request.api_request(
                omdb_base_url,
                s=search_word,
                page=page,
                apikey=api_key
            )
            if data["Response"] == "True":
                movies = data["Search"]
                for movie in movies:
                    if movie["Type"] == "movie":
                        self.insert_movie(movie)
                        movies_count += 1
                        if movies_count >= count:
                            break
            else:
                logging.info("All movies against search word {} has been extracted. "
                             "Total movies inserted in DB are {}".format(search_word, movies_count))
                break
            page += 1

    @staticmethod
    def insert_movie(movie_data):
        if "imdbID" in movie_data and movie_data["imdbID"]:
            return movie.Movie.create(
                movie_data["imdbID"],
                movie_data["Type"] if "Type" in movie_data and movie_data["Type"] else "movie",
                movie_data["Title"] if "Title" in movie_data and movie_data["Title"] else "No Title",
                movie_data["Year"] if "Year" in movie_data and movie_data["Year"] else "0000",
                movie_data["Poster"] if "Poster" in movie_data and movie_data["Poster"] else ""
            )
