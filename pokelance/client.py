import json
import random
from typing import Union, Optional

from .http import HTTPClient
from .cache import Cache
from .pokemon import Pokemon
from .errors import CacheDisabled

__all__ = ("Client",)


class Client:
    """The Client class with all the methods related to Base API.

    This class is made to define an object which would send requests and receive raw data from the API.

    Parameters
    -----------
        cache_data: :class:`bool`
            A bool identifying if the Client should cache the response from URLs on every API request or not.
    """

    def __init__(self, cache_data: bool = True) -> None:
        self.http = HTTPClient()
        self._cache = Cache(self) if cache_data else None

    @property
    def cache(self) -> Optional[Cache]:
        """Returns the :class:`.Cache` object for the :class:`.Client` if cache is enabled"""
        if not self._cache:
            raise CacheDisabled()
        return self._cache

    def save_pokemon_cache(self) -> None:
        """Save all the cached Pokémon data into a JSON file named `cached_pokemons.json`"""
        cached_data = self.cache
        with open("cached_pokemons.json", "w") as cachefile:
            json.dump(cached_data.pokemon_cache_impl, cachefile)
    
    def load_pokemon_cache(self) -> None:
        cached_data = self.cache
        with open("cached_pokemons.json", "r") as cachefile:
            data = json.load(cachefile) 
            cached_data.pokemon_cache_impl.update

    async def get_pokemon(self, pokemon: Union[int, str] = None) -> Pokemon:
        """A method used to get the Pokémon.

        This method is used to get a :class:`Pokemon` object either from the cache or the API.

        Parameters
        ----------

        pokemon: :class:`Union[int, str]`
            The id or name of the Pokémon to get data about.
            Gets a random Pokemon if no value is provided.

        Returns
        -------

        :class:`Pokemon`
        """

        if not pokemon:
            pokemon = random.randint(1, 500)
        if self._cache is not None:
            cached_data = self._cache.pokemon_cache.get(pokemon)
            if cached_data:
                return Pokemon(self, cached_data)

        data = await self.http.fetch_pokemon_data(pokemon)

        if self._cache:
            self._cache.pokemon_cache[data["id"]] = data
            self._cache.pokemon_cache[data["name"]] = data
            self._cache.sprites_cache_impl[data["id"]] = data["sprites"]
            self._cache.sprites_cache_impl[data["name"]] = data["sprites"]

        return Pokemon(self, data)
