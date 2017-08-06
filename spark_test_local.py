import os
import sys


# ************ Path for spark source folder
try:
    assert os.environ.get('SPARK_HOME')
except AssertionError as e:
    print('Please set the \'SPARK_HOME\' env variable', e)
    sys.exit(1)


# ************ Append pyspark to Python Path and import
sys.path.append("/usr/local/Cellar/apache-spark/2.1.1/libexec/python/")

try:
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("Successfully imported Spark Modules")

except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)

# ************ configuration
conf = SparkConf().setAppName('appName').setMaster('local')  # local mode
sc = SparkContext(conf=conf)


# ************* tests
def test01():
    data = range(10)
    dist_data = sc.parallelize(data)
    print dist_data.reduce(lambda a, b: a + b)


def test02(myfile):
    text_file = sc.textFile(myfile)
    # text_file = sc.textFile("hdfs://my-txt-file.txt")
    counts = text_file.flatMap(lambda line: line.split("\t")) \
                 .map(lambda word: (word, 1)) \
                 .reduceByKey(lambda a, b: a + b)

    # Executes the DAG (Directed Acyclic Graph) for counting and collecting the result
    for wc in counts.collect():
        print wc


# ************ main
if __name__ == '__main__':
    # test01()
    test02("pipeline-example/example-out.txt")

# ************ EOF
