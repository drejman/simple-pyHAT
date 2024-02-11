from dataclasses import fields
from typing import Self, Mapping

from app.domain.models import Artist
from app.repository.tinydb.CRUD import CRUD

class ArtistFactory:
    @staticmethod
    def create(data: Mapping):
        params: list[str] = [field.name for field in fields(Artist)]
        return Artist(**{k: v for k, v in data.items() if k in params})


class ArtistRepository:
    def __init__(self) -> None:
        self.artist_details = CRUD.with_table("artist_details")
        self.artist_info = CRUD.with_table("artist_info")
        self.factory = ArtistFactory()
    
    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def get_random_artist(self) -> Artist:
        artist_info = self.artist_info.get_random_item()
        return self._join_artist_data(artist_info=artist_info)
    
    def get_all_artists(self) -> list[Artist]:
        artists_info = self.artist_info.all_items()
        artists = [self._join_artist_data(artist_info=artist_info) for artist_info in artists_info]
        return artists

    def get_artist(self, id: int) -> Artist:
        artist_info = self.artist_info.find(key="id", value=id)[0]
        return self._join_artist_data(artist_info=artist_info)

    def _join_artist_data(self, artist_info: dict, join_key: str = "id") -> Artist:
        artist_data = self.artist_details.find(key=join_key, value=artist_info[join_key])[0]
        artist_data |= artist_info
        return self.factory.create(artist_data)
    
    def search_names(self, search: str) -> list[Artist]:
        search_results = self.artist_details.search(key="name", value=search)
        if search_results:
            return [self.factory.create(data=data) for data in search_results]

