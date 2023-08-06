from geopy import Nominatim
from geopy.adapters import AioHTTPAdapter


async def coords_to_location(latitude: float, longitude: float) -> str:
    async with Nominatim(user_agent='b_b', adapter_factory=AioHTTPAdapter) as locator:
        location = await locator.reverse((latitude, longitude), zoom=10)
        return location.raw['address']['city']
