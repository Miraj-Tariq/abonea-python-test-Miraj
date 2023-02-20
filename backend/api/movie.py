from backend import api, movie
from backend.oauth2 import oauth2
from backend.swagger import swagger
from backend.wsgi import remote, messages, message_types


class AddMovieRequest(messages.Message):
    title = messages.StringField(1, required=True)
    year = messages.StringField(2)
    imdb_id = messages.StringField(3)
    type = messages.StringField(4)
    image = messages.StringField(5)


class GetMovieByTitleRequest(messages.Message):
    title = messages.StringField(1, required=True)


class MovieResponse(messages.Message):
    id = messages.StringField(1)
    title = messages.StringField(2)
    year = messages.StringField(3)
    imdb_id = messages.StringField(4)
    type = messages.StringField(5)
    image = messages.StringField(6)


class ListMovieRequest(messages.Message):
    limit = messages.IntegerField(1, default=10)
    offset = messages.IntegerField(2, default=0)


class ListMovieResponse(messages.Message):
    limit = messages.IntegerField(1, required=True)
    offset = messages.IntegerField(2, required=True)
    movies_list = messages.MessageField(MovieResponse, 3, repeated=True, required=False)


class DeleteMovieRequest(messages.Message):
    id = messages.StringField(1, required=True)


@api.endpoint(path="movie", title="Movie API")
class Movie(remote.Service):
    @swagger("Add movie")
    @remote.method(AddMovieRequest, MovieResponse)
    def create(self, request):
        if all((request.title, request.year, request.imdb_id, request.type, request.image)):
            new_movie = movie.Movie.create(
                title=request.title,
                year=request.year,
                imdb_id=request.imdb_id,
                type=request.type,
                image=request.image
            )
        else:
            new_movie = movie.Movie.create_by_title(request.title)
        return MovieResponse(
            id=new_movie.id,
            title=new_movie.title,
            year=new_movie.year,
            imdb_id=new_movie.imdb_id,
            type=new_movie.type,
            image=new_movie.image
        )

    @swagger("Get movie by title")
    @remote.method(GetMovieByTitleRequest, MovieResponse)
    def get(self, request):
        movie_found = movie.Movie.read_by_title(title=request.title)
        return MovieResponse(
            id=movie_found.id,
            title=movie_found.title,
            year=movie_found.year,
            imdb_id=movie_found.imdb_id,
            type=movie_found.type,
            image=movie_found.image
        )

    @swagger("Get list of movies")
    @remote.method(ListMovieRequest, ListMovieResponse)
    def list(self, request):
        movies = movie.Movie.get_movies_list(
            offset=request.offset, limit=request.limit
        )
        return ListMovieResponse(
            offset=request.offset,
            limit=request.limit,
            movies_list=[MovieResponse(
                id=m.id,
                title=m.title,
                year=m.year,
                imdb_id=m.imdb_id,
                type=m.type,
                image=m.image
            ) for m in movies],
        )

    @swagger("Delete movie")
    @oauth2.required()
    @remote.method(DeleteMovieRequest, message_types.VoidMessage)
    def delete(self, request):
        movie.Movie.read_by_id(imdb_id=request.id).delete()
        return message_types.VoidMessage()
