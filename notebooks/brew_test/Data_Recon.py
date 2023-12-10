# Databricks notebook source
from pyspark.sql.functions import sum, col
from pyspark.sql.types import IntegerType

# COMMAND ----------

# MAGIC %run brew_test/setup/configurations

# COMMAND ----------

df_bronze = spark.read.json(bronze_path)
df_silver = spark.read.parquet(silver_path)
df_gold = spark.read.parquet(gold_path)

# COMMAND ----------

df_gold.schema

# COMMAND ----------

df_bronze.display()

# COMMAND ----------

df_silver.display()

# COMMAND ----------

df_gold.dtypes

# COMMAND ----------

# DBTITLE 1,Converting store_count values to int
df_gold = df_gold.withColumn('store_count', col('store_count').cast(IntegerType()))

# COMMAND ----------

# DBTITLE 1,Checking the row counting
bronze_count = df_bronze.count()
silver_count = df_silver.count()
gold_count = df_gold.agg(sum('store_count')).collect()[0][0]
print("Row count in bronze layer: ", bronze_count)
print("Row count in silver layer: ", silver_count)
print("total count in gold layer aggregations: ", gold_count)

# COMMAND ----------

