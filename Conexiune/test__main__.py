# def test_args_kwargs(arg1, *args):
#     print("arg1:", arg1)
#     for arg in args:
#         print(arg)
#
#
# test_args_kwargs()
from geopy import Nominatim


def start():
    geoloc = Nominatim(user_agent='brg_application')
    res = geoloc.reverse((54.761516, 20.497211), zoom=10)
    city = res.raw['address']['city']
    print(5)


start()
