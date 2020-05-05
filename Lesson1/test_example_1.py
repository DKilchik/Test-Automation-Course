#!/usr/bin/python3
# -*- encoding=utf8 -*-

import requests
from time import perf_counter


def timer(func):
    def wrapper(*args):
        t_start = perf_counter()
        result = func(*args)
        t_stop = perf_counter()
        print("Время выполнения теста:", t_stop - t_start)
        return result

    return wrapper


@timer
def test_check_country():  # Test 1
    result = requests.get('http://ip-api.com/json')
    data = result.json()

    countrylist = ['Republic of Moldova', "Russia", "Russian Federation", "Moldova", "Ukraine", "United States",
                   "United Kingdom", "China"]
    # Creating primitive Country List
    country = data.get('country')

    assert country in countrylist, "Country Not Found In Country List!"  # Check if Country List include my country


@timer
def test_check_provider():  # Test 2(Error test)
    result = requests.get('http://ip-api.com/json')
    data = result.json()

    provmol = ["SC STARNET SRL", "JSC MOLDTELECOM SA"]  # List Of Moldavian Providers
    provrus = ["NOVOE-KTV", "JSC Ufanet Kazan branch"]  # List Of Russian Providers

    country = data.get('country')
    isp = data.get('isp')

    if country == "Russia":  # Check User's Country.Get Provider's list of detected country.
        provider = provrus
    else:
        provider = provmol

    assert isp in provider, "Provider does not exist in Provider List!"


@timer
def test_check_countryCode():  # Test 3
    result = requests.get('http://ip-api.com/json')
    data = result.json()

    ruscouncode = ('RU')  # Country Code for Russian users
    moldcouncode = ('MD')  # Country Code for Moldavian users

    country = data.get('country')
    countryCode = data.get('countryCode')

    if country == "Russia":  # Ckecking user's country.
        checkcountry = ruscouncode
    else:
        checkcountry = moldcouncode

    assert checkcountry == countryCode, "Wrong Country Code!"


@timer
def test_check_city():  # Test 4
    result = requests.get('http://ip-api.com/json')
    data = result.json()

    cityrus = ['Moscow', 'Cheboksary', 'Ufa', 'Kazan']  # List of Russian cities
    citymd = ['Chisinau']  # List of Moldavian cities

    country = data.get('country')
    city = data.get('city')

    if country == "Russia":  # Ckecking user's country.
        citylist = cityrus
    else:
        citylist = citymd

    assert city in citylist, "Your city does not exist in City List!"


@timer
def test_check_status():  # Test 5
    result = requests.get('http://ip-api.com/json')
    data = result.json()

    status = data.get('status')

    assert status == 'success', "Status:Error!"


@timer
def test_check_AS():  # Test 6
    result = requests.get('http://ip-api.com/json')
    data = result.json()

    autonomSys = data.get('as')

    assert len(autonomSys) > 0, "Autonomous system does not specified!"


def get_latitude(latitude):
    numbers = latitude
    f = numbers

    if f < -90 or f > 90:
        return False
    return True


def get_longitude(longitude):
    num = longitude
    b = num

    if b < -180 or b > 180:
        return False
    return True


@timer
def test_check_latlon():  # Test 7
    result = requests.get('http://ip-api.com/json')
    data = result.json()

    latitude = data.get('lat')
    longitude = data.get('lon')

    assert get_latitude(latitude)
    assert get_longitude(longitude)
