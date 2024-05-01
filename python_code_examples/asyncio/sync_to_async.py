import asyncio
from time import perf_counter

import requests


async def counter(until: int = 10) -> None:
    now = perf_counter()
    print("Started counter")
    for i in range(until):
        last = now
        await asyncio.sleep(0.1)
        now = perf_counter()
        print(f"{i} was asleep for {now - last} sec.")


# This is a blocking function
def send_request(url: str) -> int:
    print("Sending HTTP request")
    response = requests.get(url)
    return response.status_code


async def send_request_async(url: str):
    return await asyncio.to_thread(send_request, url)


async def main() -> None:
    status_code = await send_request_async("https://www.google.com")
    print(f"Got HTTP response with status {status_code}")
    await counter()

    # To run these functions, asynchronously use gather
    status_code, _ = await asyncio.gather(
        send_request_async("https://www.google.com"), counter()
    )
    print(status_code)


if __name__ == "__main__":
    asyncio.run(main())
