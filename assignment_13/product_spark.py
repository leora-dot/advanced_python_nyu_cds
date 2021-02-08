from pyspark import SparkContext
from operator import mul

if __name__ == '__main__':
    sc = SparkContext("local", "products")
    # Create an RDD of numbers from 0 to 1000
    nums = sc.parallelize(range(1, 1000))
    #Calculate product of all numbers in RDD
    prod = nums.fold(1, mul)
    print(prod)

#RUN COMMAND: spark-submit product_spark.py
