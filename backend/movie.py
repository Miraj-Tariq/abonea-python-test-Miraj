from google.cloud import ndb
from backend import error
from backend.utils import request
from backend.constants import omdb_base_url

import os
from dotenv import load_dotenv

load_dotenv()


class NotFound(error.Error):
    pass


class Movie(ndb.Model):
    title = ndb.StringProperty(indexed=True, required=True)
    normalized_title = ndb.ComputedProperty(lambda self: self.title and self.title.lower(), indexed=True)
    year = ndb.StringProperty()
    imdb_id = ndb.StringProperty(indexed=True)
    type = ndb.StringProperty()
    image = ndb.StringProperty()

    @classmethod
    def create(cls, imdb_id, type, title, year, image=""):
        entity = cls(
            imdb_id=imdb_id,
            type=type,
            title=title,
            year=year,
            image=image
        )
        entity.put()
        return entity

    def __hash__(self):
        return hash((self.__class__.__name__, self.id))

    def delete(self):
        self.key.delete()

    @property
    def id(self):
        return self.key.urlsafe().decode("utf-8")

    @classmethod
    def get_movies_list(cls, offset, limit):
        return cls.query().order(cls.title).fetch(offset=offset, limit=limit)

    @classmethod
    def read_by_id(cls, imdb_id):
        entity = cls.query(cls.imdb_id == imdb_id).get()
        if entity is None or not isinstance(entity, cls):
            raise NotFound("No movie found with id: {}".format(imdb_id))
        return entity

    @classmethod
    def read_by_title(cls, title):
        entity = cls.query().filter(
            cls.normalized_title >= title.lower(),
            cls.normalized_title < title.lower() + "\uFFFD"
        ).get()
        if entity is None or not isinstance(entity, cls):
            raise NotFound("No movie found with title: {}".format(title))
        return entity

    @classmethod
    def create_by_title(cls, title):
        data = request.api_request(
            omdb_base_url,
            t=title,
            apikey=os.getenv("OMDB_KEY")
        )
        if data["Response"] == "True":
            return cls.create(
                data["imdbID"],
                data["Type"],
                data["Title"],
                data["Year"],
                data["Poster"]
            )
        else:
            raise NotFound("No movie found with title: {}".format(title))

    @classmethod
    def count(cls):
        return cls.query().count()
