from backend import test, movie


class TestMovie(test.TestCase):
    def test_create(self):
        new_movie = movie.Movie.create(
            title="A Christmas Star",
            year="2015",
            imdb_id="tt4591840",
            type="movie",
            image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
        )
        self.assertEqual(new_movie, movie.Movie.read_by_id(new_movie.imdb_id))
        self.assertTrue(new_movie.title == "A Christmas Star")
        self.assertTrue(new_movie.year == "2015")
        self.assertTrue(new_movie.imdb_id == "tt4591840")
        self.assertTrue(new_movie.type == "movie")
        self.assertTrue(new_movie.image == "https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg")

    def test_read_by_id(self):
        new_movie = movie.Movie.create(
            title="A Christmas Star",
            year="2015",
            imdb_id="tt4591840",
            type="movie",
            image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
        )
        self.assertEqual(new_movie, movie.Movie.read_by_id(imdb_id="tt4591840"))
        with self.assertRaises(movie.NotFound):
            movie.Movie.read_by_id(imdb_id="tt4591841")

    def test_read_by_title(self):
        new_movie = movie.Movie.create(
            title="A Christmas Star",
            year="2015",
            imdb_id="tt4591840",
            type="movie",
            image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
        )
        self.assertEqual(new_movie, movie.Movie.read_by_title(title="A Christmas Star"))
        # self.assertEqual(new_movie, movie.Movie.read_by_title(title="Christmas"))
        with self.assertRaises(movie.NotFound):
            movie.Movie.read_by_title(title="Inception")

    def test_delete_by_id(self):
        new_movie = movie.Movie.create(
            title="A Christmas Star",
            year="2015",
            imdb_id="tt4591840",
            type="movie",
            image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
        )
        new_movie.delete()
        with self.assertRaises(movie.NotFound):
            movie.Movie.read_by_id(imdb_id=new_movie.imdb_id)

    def test_get_movies_list(self):
        movie.Movie.create(
            title="The Godfather",
            year="1972",
            imdb_id="tt0068646",
            type="movie",
            image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
        )
        movie.Movie.create(
            title="12 Angry Men",
            year="1957",
            imdb_id="tt0050083",
            type="movie",
            image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
        )
        movie.Movie.create(
            title="Forest Gump",
            year="1994",
            imdb_id="tt0109830",
            type="movie",
            image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
        )

        movies = movie.Movie.get_movies_list(offset=0, limit=10)
        self.assertEqual(3, len(movies))
        self.assertEqual("12 Angry Men", movies[0].title)

        paginated_movies = movie.Movie.get_movies_list(offset=1, limit=2)
        self.assertEqual(2, len(paginated_movies))
        self.assertEqual("The Godfather", paginated_movies[-1].title)

    def test_create_by_title(self):
        new_movie = movie.Movie.create_by_title(title="Inception")
        self.assertEqual(new_movie, movie.Movie.read_by_title(title="Inception"))
        self.assertEqual(new_movie.title, movie.Movie.read_by_title(title="Inception").title)
        with self.assertRaises(movie.NotFound):
            movie.Movie.read_by_title(title="Interstellar")

    def test_count(self):
        movie.Movie.create(
            title="A Christmas Star",
            year="2015",
            imdb_id="tt4591840",
            type="movie",
            image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
        )
        self.assertEqual(1, movie.Movie.count())


class TestMovieApi(test.TestCase):

    def test_create(self):
        resp = self.api_client.post(
            "movie.create",
            dict(
                title="A Christmas Star",
                year="2015",
                imdb_id="tt4591840",
                type="movie",
                image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
            )
        )
        self.assertEqual("A Christmas Star", resp["title"])
        self.assertEqual("2015", resp["year"])
        self.assertEqual("tt4591840", resp["imdb_id"])
        self.assertEqual("movie", resp["type"])
        self.assertEqual("https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg", resp["image"])

    def test_get(self):
        self.api_client.post(
            "movie.create",
            dict(
                title="A Christmas Star",
                year="2015",
                imdb_id="tt4591840",
                type="movie",
                image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
            )
        )
        resp = self.api_client.post("movie.get", dict(title="A Christmas Star"))
        self.assertEqual("A Christmas Star", resp["title"])

        resp = self.api_client.post("movie.get", dict(title="Interstellar"))
        self.assertEqual(True, bool(resp.get("error")))

    def test_list(self):
        self.api_client.post(
            "movie.create",
            dict(
                title="The Godfather",
                year="1972",
                imdb_id="tt0068646",
                type="movie",
                image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
            )
        )
        self.api_client.post(
            "movie.create",
            dict(
                title="12 Angry Men",
                year="1957",
                imdb_id="tt0050083",
                type="movie",
                image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
            )
        )
        self.api_client.post(
            "movie.create",
            dict(
                title="Forest Gump",
                year="1994",
                imdb_id="tt0109830",
                type="movie",
                image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
            )
        )

        resp = self.api_client.post("movie.list")
        self.assertEqual(3, len(resp["movies_list"]))
        self.assertEqual(10, resp["limit"])
        self.assertEqual(0, resp["offset"])

        resp = self.api_client.post(
            "movie.list", dict(limit=2, offset=1)
        )
        self.assertEqual(2, len(resp["movies_list"]))
        self.assertEqual(2, resp["limit"])
        self.assertEqual(1, resp["offset"])
        self.assertEqual("Forest Gump", resp.get("movies_list")[0].get("title"))

    def test_delete(self):
        new_movie = self.api_client.post(
            "movie.create",
            dict(
                title="A Christmas Star",
                year="2015",
                imdb_id="tt4591840",
                type="movie",
                image="https://m.media-amazon.com/images/M/MV5BNjcxMDU4ODg5N15BMl5BanBnXkFtZTgwODc2MjU5OTE@._V1_SX300.jpg"
            )
        )
        movie_resp = self.api_client.post(
            "movie.delete", dict(id=new_movie["imdb_id"])
        )
        self.assertEqual(True, bool(movie_resp["error"]))

        user_response = self.api_client.post(
            "user.create", dict(email="test@gmail.com", password="test")
        )
        access_token = user_response["access_token"]
        movie_resp = self.api_client.post(
            "movie.delete",
            dict(id=new_movie["imdb_id"]),
            headers=dict(authorization=access_token),
        )
