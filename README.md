

**Give some documentation on why you chose what you did.**

- I chose Python because is very a very usual language in testing and quite spread.
- Besides it is not appropiated and nice to have all code in one file, I tried to answer the questions in order so it is easy to follow and review.
- I added some basic unit tests in order to fill that gap in the testing scope of this API.
- I didn&#39;t add try-catch because I feel that complicates the core of the methods and code in general when it comes to testing. However for a long term testing I would use it.
- As the return of each method I tried to use a standard criteria: either the full response of the request or the most obvious result of the method (random value we seek, array of bookings, number of processed users of a test, etc)
- Besides I returned the processed users of the performance tests, it would be better for a long term testing, returning a dictionary with the values we consider best: CPU, memory, delay, etc).
- I decided to add some performance measurements in the tests in order to get more information than just the number of proccessed users, however those samples should be taken from a different method running in parallel or better: from a framework tailored made for this API.
- I added a DEBUG flag that should be enabled in order to get more feedback about what is actually happening or when some tests are failing and we want to debug the tests or code. When the DEBUG in activated, the performance is lower, so we recommend to disable this flag when running performance tests.
-For the airports reading from a file, I took a json file with airport information from https://github.com/mwgg/Airports, however I had to remove or modify some entries that raised errors (numbers, lowercase, symbols, etc)
-I didn't add try-catch because I feel that complicates the core of the methods and code in general when it comes to testing. However for a long term testing I would use it. I did a small error control when the request was not ok, displaying request and response, which was quite helpful to detect some errors form the airports json I took from internet.

**How to run these tests.**

Clone the code from git.
```
git clone $repo
```
You can run it by calling python:
```
python booking_performance.py
```
Or give execution permissions and run it:
```
chmod +x booking_performance.py
./booking_performace.py
```
For running the unit tests that were not requested:
```
./booking_unittests.py
```

Low performance test with debugging information:
```
booking_carrey.py
```
High performnace test:
```
booking_norris.py
```


**Show reporting for your results.**

The tests are made to return the raw information in other to plot it and storage it in a database. However, for a quick feedback and for those prompt lovers, there is basic text output during and/or at the end of the test.
```
Starting load test. 30 concurrent users during 1 minutes.

Load test. 120 users were created in 1 minutes with 100.0 % CPU (120 samples)
```

```
Starting distribution load test with pattern [[1, 1], [3, 1], [0, 1], [1, 1]]

Rate: 1u/sec         Duration: 1 minutes.

Distributed load test. 56 users were created with 95.0 % CPU (56 samples)

Rate: 3u/sec         Duration: 1 minutes.

Distributed load test. 153 users were created with 96.0 % CPU (49 samples)

Rate: 0u/sec         Duration: 1 minutes.

Distributed load test. 153 users were created with 95.0 % CPU (58 samples)

Rate: 1u/sec         Duration: 1 minutes.

Distributed load test. 210 users were created with 96.0 % CPU (57 samples)
```

