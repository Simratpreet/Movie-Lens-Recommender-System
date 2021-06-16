
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, regexp_replace, trim, col, countDistinct, substring, desc
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, DoubleType, StringType, StructField
from utils import compute_item_similarity
import logging

spark = SparkSession.builder.appName("Recommender").getOrCreate()
spark.conf.set('spark.files', 'Movie Lens Recommendation and Analytics/security/secure-connect-simrat-personal.zip')
spark.conf.set('spark.cassandra.connection.config.cloud.path', 'secure-connect-simrat-personal.zip')
spark.conf.set('spark.cassandra.auth.username', <<CLIENT_ID>>)
spark.conf.set('spark.cassandra.auth.password', <<CLIENT_PASS>>)
spark.conf.set('spark.dse.continuousPagingEnabled', 'false')

spark.sparkContext.setLogLevel("ERROR") 
logger = logging.getLogger('py4j')

# read data from s3
movie_df = spark.read.options(header='true').csv('s3://big-data-bucket-simrat/data/ml-25m/movies.csv')
rating_df = spark.read.options(header='true').csv('s3://big-data-bucket-simrat/data/ml-25m/ratings.csv')

# clean data
movie_df = movie_df.withColumn('year', substring('title', -5, 4))
movie_df = movie_df.drop('genres')
rating_df = rating_df.drop('timestamp')
rating_df = rating_df.withColumn('rating', col('rating').cast('float'))

# bring titles to rating_df
rating_df = rating_df.join(movie_df, on='movieId', how='left').drop('movieId', 'year')
trimmed_rat_df = rating_df.limit(100000)

# calculate cosine similarity basis item-item comparison of user ratings
sim_df = compute_item_similarity(trimmed_rat_df, 'userId', 'title', 'rating')
print("Computed similarity")
sim_df = sim_df.limit(1000)
print(sim_df.count())

# write data to cassandra
for i in range(0, 2):
    try:
        sim_df.write.format("org.apache.spark.sql.cassandra").options(table='similarity', keyspace='simrat_personal_keyspace').save()
        print("Written to Cassandra")
        break
    except:
        continue