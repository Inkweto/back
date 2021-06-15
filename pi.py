# import random
# from pyspark import SparkContext
# import requests

# NUM_SAMPLES = 100000000

# def inside(p):
#     x, y = random.random(), random.random()
#     return x*x + y*y < 1


# sc = SparkContext.getOrCreate()
# count = sc.parallelize(range(0, NUM_SAMPLES)) \
#     .filter(inside).count()
# print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))

# url = 'http://localhost:5000/result/'

# myobj = {'search_phrase': 'a',
#          'line': '2',
#          'date': '2021-01-01T23:30:00',
#          'content': 'qqq'}

# x = requests.post(url, data = myobj)

# print(x.text)