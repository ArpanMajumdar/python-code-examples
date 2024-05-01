import asyncio
from random import randint
from time import perf_counter

from req_http import http_get_async, http_get_sync

MAX_POKEMON_ID = 898


def get_random_pokemon_name_sync() -> str:
    pokemon_id = randint(1, MAX_POKEMON_ID)
    pokemon_api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = http_get_sync(pokemon_api_url)
    return str(response["name"])


async def get_random_pokemon_name_async() -> str:
    pokemon_id = randint(1, MAX_POKEMON_ID)
    pokemon_api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = await http_get_async(pokemon_api_url)
    return str(response["name"])


# We can also use async generator functions
async def get_next_pokemons(count: int):
    for _ in range(count):
        name = await get_random_pokemon_name_async()
        yield name


# def main() -> None:
#     pokemon_name = get_random_pokemon_name_sync()
#     print(pokemon_name)


async def main() -> None:
    # This still runs syncronously as we are waiting after each async call to make the next call
    print("Synchronous requests example")
    start_time = perf_counter()
    for _ in range(20):
        pokemon_name = await get_random_pokemon_name_async()
        print(pokemon_name)
    end_time = perf_counter()
    print(f"Time taken(synchronous): {end_time - start_time}")
    print()

    # This runs concurrently as we fire all the requests at once and wait for them later
    print("Asynchronous requests example")
    start_time = perf_counter()
    deferred_pokemon_names = [get_random_pokemon_name_async() for _ in range(20)]
    result = await asyncio.gather(*deferred_pokemon_names)
    print(result)
    end_time = perf_counter()
    print(f"Time taken(asynchronous): {end_time - start_time}")
    print()

    # Async generator function
    print("Async generator function")
    async for name in get_next_pokemons(20):
        print(name)

    print()

    # Asynchronous list comprehensions
    print("Async list comprehensions")
    names = [name async for name in get_next_pokemons(20)]
    print(names)
    print()


if __name__ == "__main__":
    asyncio.run(main())
