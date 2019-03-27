#!/usr/bin/env python3
"""Unit tests for booking API"""

from __future__ import print_function
import json
import unittest
import requests

HOST_IP = '192.168.1.38'
HOST_PORT = '8900'
API_URL = 'http://' + HOST_IP + ':' + HOST_PORT

class TestStringMethods(unittest.TestCase):
    """Unit tests for booking API"""
    def test_booking_get_200(self):
        """Booking get UT for code 200"""
        response = requests.get(API_URL + "/booking", params={"id": "12", "date": "2019-12-21"})
        if response.status_code != 200:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_booking_get_400(self):
        """Booking get UT for code 400"""
        response = requests.get(API_URL + "/booking")
        if response.status_code != 400:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 400)

    def test_booking_get_500(self):
        """Booking get UT for code 500"""
        response = requests.get(API_URL + "/booking", params={"id": "12", "date": "19-12-2019"})
        if response.status_code != 500:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 500)

    def test_booking_post_201(self):
        """Booking post UT for code 201"""
        data = {"date": "2020-01-01",
                "destination": "AMS",
                "id": "pepe@pepe.pe1-0.2",
                "origin": "MAD"}
        response = requests.post(API_URL + '/booking', data=json.dumps(data),
                                 headers={'Content-Type': 'application/json', \
                                 'Accept': 'application/json'})
        if response.status_code != 201:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 201)

    def test_booking_post_409(self):
        """Booking post UT for code 409"""
        data = {"date": "2020-01-01",
                "destination": "amsterdam",
                "id": "pepe@pepe.pe1-0.2",
                "origin": "MAD"}
        response = requests.post(API_URL + '/booking', data=json.dumps(data),
                                 headers={'Content-Type': 'application/json', \
                                 'Accept': 'application/json'})
        if response.status_code != 409:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 409)

    def test_user_get_200(self):
        """User get UT for code 200"""
        response = requests.get(API_URL + "/user", params={"id" : "pepe@pepe.pe1-0.1"})
        if response.status_code != 200:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 200)


    def test_user_get_404(self):
        """User get UT for code 404"""
        response = requests.get(API_URL + "/user", params={"id" : "pepe"})
        if response.status_code != 404:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 404)

    def test_user_get_500(self):
        """User get UT for code 500"""
        response = requests.get(API_URL + "/user", params={})
        if response.status_code != 500:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 500)


    def test_user_post_201(self):
        """User get UT for code 201"""
        data = {"email": "john@gmail.com",
                "name": "john"}
        response = requests.post(API_URL + '/user', data=json.dumps(data),
                                 headers={'Content-Type': 'application/json', \
                                 'Accept': 'application/json'})
        if response.status_code != 201:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 201)

    def test_user_post_409(self):
        """User get UT for code 409"""
        data = {}
        response = requests.post(API_URL + '/user', data=json.dumps(data),
                                 headers={'Content-Type': 'application/json', \
                                 'Accept': 'application/json'})
        if response.status_code != 409:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 409)

    def test_user_post_500(self):
        """User post UT for code 500"""
        data = {"email": "johngmail.com",
                "name": "john"}
        response = requests.post(API_URL + '/user', data=json.dumps(data),
                                 headers={'Content-Type': 'application/json', \
                                 'Accept': 'application/json'})
        if response.status_code != 500:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 500)

    def test_userall_get_200(self):
        """User get UT for code 200"""
        response = requests.get(API_URL + "/user/all", params={})
        if response.status_code != 200:
            print(response)
            print(response.text)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    #unittest.main()
    UT_SUITE = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(UT_SUITE)
