#!/usr/bin/env python3
"""Assignment auxiliary functions"""

from __future__ import print_function
import json
from datetime import datetime
from datetime import timedelta
from time import sleep
import random
import string
import threading
import time
import psutil
from nose.tools import assert_true
import requests

HOST_IP = '127.0.0.1'
HOST_PORT = '8900'
API_URL = 'http://' + HOST_IP + ':' + HOST_PORT

# Set to False when running performance tests, True for debugging
VERBOSE = False

# False: takes city iata names from file as requested
# True: takes a random city name without readinf from file
HIGH_PERFORMANCE = False

#############
# USE CASES #
#############
# Creation of one user (post)
def create_user(name, email):
    """Creation of one use"""
    data = {"email": email,
            "name": name}
    if VERBOSE:
        print("\nCreating user: " + str(name))
    response = requests.post(API_URL + '/user',
                             data=json.dumps(data),
                             headers={'Content-Type': 'application/json', \
                             'Accept': 'application/json'})
    if not response.ok:
        print("Operation create_user failed with error: ")
        print(response.text)
        print("Data sent: ")
        print(data)
    return response

# Assign one booking to one user (post)
def assign_booking(date, destination, id_user, origin):
    """Assign one booking to one user"""
    data = {"date": date,
            "destination": destination,
            "id": id_user,
            "origin": origin}
    if VERBOSE:
        print("\nAssigning booking for user " + id_user)
    response = requests.post(API_URL + '/booking',
                             data=json.dumps(data),
                             headers={'Content-Type': 'application/json', \
                             'Accept': 'application/json'})
    if not response.ok:
        print("Operation assign_booking failed with error: ")
        print(response.text)
        print("Data sent: ")
        print(data)
    return response

# List of users (get)
def list_users():
    """List of users"""
    response = requests.get(API_URL + '/user/all')
    if VERBOSE:
        print("\nDisplaying users: ")
        for user in response.json():
            print("User: " + str(user["name"]) + "\tEmail: " +
                  str(user["email"]) + "\tID: " + str(user["id"]))
    if not response.ok:
        print("Operation flist_users flist_users failed with error: ")
        print(response.text)
    return response

# Bookings from one user (get)
# Best given parameter would be the id which is unique.
# For this example we will use the name in order to simplify
def show_user_bookings(id_user):
    """Bookings from one user"""
    params = {"id": id_user}
    print("\nGetting bookings for user : " + str(id_user))
    response = requests.get(API_URL + '/user', params)
    for booking in response.json()["bookings"]:
        print("Booking: " + str(booking["date"]) + "\tOrigin: " + str(
            booking["origin"]) + "\tDestination: " + str(booking["destination"]))
    if not response.ok:
        print("Operation show_user_bookings failed with error: ")
        print(response.text)
        print("Data sent: ")
        print(params)
    return response

# Random methods for mocking tests
def random_string(random_length):
    """Generate a random string of a given length """
    lowercases = string.ascii_lowercase
    random_value = ''.join(random.choice(lowercases)
                           for i in range(random_length))
    return random_value


def random_date():
    """Generates random date of the future"""
    start = datetime.now().strftime('%Y-%m-%d %H:%M')
    end = "9999-12-31 23:59"
    format_date = '%Y-%m-%d %H:%M'
    start_time = time.mktime(time.strptime(start, format_date))
    end_time = time.mktime(time.strptime(end, format_date))
    raw_time = start_time + random.random() * (end_time - start_time)
    random_time = time.strftime(format_date, time.localtime(raw_time))
    return random_time


def random_email(random_length):
    """Generates a random email"""
    return random_string(random_length) + "@" + random_string(random_length) + ".com"

# Provides random and likely unvalid city names
# More combinations and better performance for load tests
def random_city():
    """Generates a random city with IATA format. High performance"""
    random_value = random_string(3).upper()
    return random_value

# Provides valid city names
def file_city():
    """Generates a city name from a file. Low performance"""
    with open('airports_fixed.json') as json_file:
        data = json.load(json_file)
        random_int = int(random.randint(0, len(data)))
        valid_city = data[random_int]["iata"]
    return valid_city

#############
# TEST FLOW #
#############
def test_flow():
    """Test flow as requested in the assignment"""
    # 1.- Create one user
    response = create_user(random_string(16), random_email(16))
    id_user = response.json()["id"]

    # 2.- Create two bookings for that user, one with past date and another one
    # with todays date. Feed origin and destination from a file and create random booking.
    today = datetime.now()
    past_date = datetime.now() - timedelta(days=random.randint(0, 118*12*30))
    
    if HIGH_PERFORMANCE:
        assign_booking(past_date.strftime('%Y-%m-%d %H:%M'),
                       random_city(), id_user, random_city())
        assign_booking(today.strftime('%Y-%m-%d %H:%M'),
                       random_city(), id_user, random_city())
    else:
        assign_booking(past_date.strftime('%Y-%m-%d %H:%M'),
                       file_city(), id_user, file_city())
        assign_booking(today.strftime('%Y-%m-%d %H:%M'),
                       file_city(), id_user, file_city())

    # 3.- Get all today bookings.
    show_today_bookings()
    # show_today_bookings_user(id_user)

    # 4.- From all user list choose randomly one of them and get all bookings.
    show_random_user_bookings()

# 3.- Get all today bookings.
def show_today_bookings():
    """Get all today bookings"""
    response = requests.get(API_URL + '/user/all')
    if VERBOSE:
        print("\nDisplaying today bookings: ")
    users = response.json()
    today_bookings = []
    for user in users:
        for booking in user["bookings"]:
            if booking["date"] == datetime.now().strftime('%Y-%m-%d %H:%M'):
                today_bookings.append(booking)
                if VERBOSE:
                    print("User: " + str(booking["idUser"]) + "\tBooking: " \
                        + str(booking["idBooking"]) + "\tOrigin: " + str(
                            booking["origin"]) + "\tDestination: " + str(booking["destination"]))
    return today_bookings


def show_today_bookings_user(id_user):
    """Get all today bookings for a given user"""
    params = {"date": datetime.now().strftime('%Y-%m-%d %H:%M'),
              "id": id_user}
    print("\nGetting today's bookings : ")
    response = requests.get(API_URL + '/user', params)
    for booking in response.json()["bookings"]:
        print("Booking: " + str(booking["idBooking"]) + "\tOrigin: " + str(
            booking["origin"]) + "\tDestination: " + str(booking["destination"]))
    if not response.ok:
        print("Operation show_today_bookings_user failed with error: ")
        print(response.text)
        print("Data sent: ")
        print(params)
    return response

# 4.- From all user list choose randomly one of them and get all bookings.
def show_random_user_bookings():
    """From all user list choose randomly one of them and get all bookings"""
    response = requests.get(API_URL + '/user/all')
    users = response.json()
    random_int = int(random.randint(0, len(users)-2))
    random_user = users[random_int]
    bookings = random_user["bookings"]
    if VERBOSE:
        print("\nDisplaying bookings of random user: " +
              str(random_user["name"]))
        for booking in bookings:
            print("Booking: " + str(booking["idBooking"]) + "\tOrigin: " + str(
                booking["origin"]) + "\tDestination: " + str(booking["destination"]))
    if not response.ok:
        print("Operation show_random_user_bookings failed with error: ")
        print(response.text)
        print("Data sent: ")
        print(response)
    return bookings

##################
# TEST SCENARIOS #
##################
# We consider an iteration means a user creation and booking
# 1.- Unit test scenario: one user, one iteration.
# test_flow()

def basic_test():
    """Basic test (not requested in the assignment)"""
    response = create_user(random_string(16), random_email(16))
    if not response.ok:
        print("Basic test. One user, one interation. FAIL")
        return False
    id_user = response.json()["id"]
    response = assign_booking(
        random_date(), random_city(), id_user, random_city())
    if not response.ok:
        print("Basic test. One user, one interation. FAIL")
        return False
    if VERBOSE:
        print("Basic test. One user, one interation. PASS")
    return True

# 2.- Load test scenario: ten users, duration=5 minutes.
def load_test(users, duration):
    """Load test scenario"""
    print("Starting load test. " + str(users) +
          " concurrent users during " + str(duration) + " minutes.")
    threads = list()
    end = datetime.now() + timedelta(minutes=duration)
    init_users = len(list_users().json())
    total_cpu = 0.0
    samples = 0
    while datetime.now() < end:
        for user in range(users):
            test_thread = threading.Thread(target=test_flow)
            #test_thread = threading.Thread(target=basic_test)
            threads.append(test_thread)
            test_thread.start()
            #sleep(0.05)
            cpu = psutil.cpu_percent(interval=None)
            total_cpu = cpu + total_cpu
            samples += 1
    avg_cpu = round(total_cpu / samples)
    total_users = len(list_users().json()) - init_users
    print("Load test. " + str(total_users) + " users were created in "
          + str(duration) + " minutes with " + str(avg_cpu)
          + " % CPU (" + str(samples) + " samples)")
    return total_users

# 3.- Distributed load test scenario: start 1 request per second, increase to 3
# in one minute, hold for one minute, decrease to 1 in one minute.
# Creates rate users in a second
def create_users(rate):
    """Creates users at a given rate"""
    end = datetime.now() + timedelta(seconds=1)
    user = 0
    while datetime.now() < end:
        if user < rate:
            # basic_test()
            test_flow()
            user += 1

def distributed_load_test(distribution):
    """Distributed load by pairs rate,duration"""
    print("Starting distribution load test with pattern " + str(distribution))
    init_users = len(list_users().json())
    total_cpu = 0.0
    samples = 0
    total_users = 0
    for iteration in distribution:
        total_cpu = 0.0
        samples = 0
        rate = iteration[0]
        duration = iteration[1]
        print(str(rate) + "users \tDuration: " +
              str(duration) + " minutes.")
        end = datetime.now() + timedelta(minutes=duration)
        user = 0
        while datetime.now() < end:
            while user < rate:
                test_flow()
                user += 1
                cpu = psutil.cpu_percent(interval=None)
                total_cpu = cpu + total_cpu
                samples += 1
            sleep(0.1)
        avg_cpu = round(total_cpu / samples)
        total_users = len(list_users().json()) - init_users
        print("Distributed load test. " + str(total_users) + " users were created with " +
              str(avg_cpu) + " % CPU (" + str(samples) + " samples)")
    return total_users
