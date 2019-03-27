#!/usr/bin/env python3
"""Only performance tests"""

#from booking_functions.py import *
import booking_functions

booking_functions.VERBOSE = True

# 2.- Load test scenario: 3 users, duration=1 minute.
booking_functions.load_test(3, 1)

# 3.- Distributed load test scenario:
# start 1 request per second,
# increase to 2 in one minute.
booking_functions.distributed_load_test([[1, 1], [2, 1]])
