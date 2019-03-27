#!/usr/bin/env python3
"""Only performance tests"""

#from booking_functions.py import *
import booking_functions

# 1.- Unit test scenario: one user, one iteration.
booking_functions.test_flow()

# 2.- Load test scenario: ten users, duration=5 minutes.
booking_functions.load_test(10, 5)

# 3.- Distributed load test scenario:
# start 1 request per second,
# increase to 3 in one minute,
# hold for one minute,
# decrease to 1 in one minute.
booking_functions.distributed_load_test([[1, 1], [3, 1], [0, 1], [1, 1]])
