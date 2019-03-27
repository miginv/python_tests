#!/usr/bin/env python3
"""Only performance tests"""

#from booking_functions.py import *
import booking_functions

#booking_functions.HIGH_PERFORMANCE = True

# 2.- Load test scenario: 100 users, duration=1 minute.
booking_functions.load_test(10, 1)

# 3.- Distributed load test scenario:
# start 200 request per second,
# increase to 300 in one minute.
booking_functions.distributed_load_test([[20, 1]])
