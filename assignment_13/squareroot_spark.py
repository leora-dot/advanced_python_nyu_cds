from pyspark import SparkContext
from operator import add
import numpy as np

if __name__ == '__main__':
    sc = SparkContext("local", "products")
    #Create an RDD of numbers from 0 to 1000
    nums = sc.parallelize(range(1, max_val))
    #Calculate square roots
    square_roots = nums.map(lambda val: np.sqrt(val))
    #Calculate average of square roots
    average = square_roots.fold(0, add) / square_roots.count()
    #Print solution
    print(average)

#RUN COMMAND: spark-submit squareroot_spark.py
