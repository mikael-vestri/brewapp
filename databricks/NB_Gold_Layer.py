# Databricks notebook source
from pyspark.sql.functions import count, col
from pyspark.sql.types import IntegerType

# COMMAND ----------

# MAGIC %run ../setup/configurations

# COMMAND ----------

# DBTITLE 1,Reading data from silver layer
df_silver = spark.read.parquet(silver_path)

# COMMAND ----------

# DBTITLE 1,Applying data transformation and aggregations
df_gold = df_silver\
    .groupBy("brewery_type", "state")\
    .agg(count("id").alias("store_count"))\
    .withColumn('store_count', col('store_count').cast(IntegerType()))

# COMMAND ----------

# DBTITLE 1,Writing data to gold layer in blob storage
df_gold.write.format("parquet").mode("overwrite").save(gold_path)

# COMMAND ----------

