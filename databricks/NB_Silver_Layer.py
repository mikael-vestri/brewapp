# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType, DoubleType

# # Crie uma Spark session
# spark = SparkSession.builder.appName("ExemploEscritaParticionada").getOrCreate()

# # Configurar o tamanho máximo de partição em bytes (exemplo: 128 MB)
# spark.conf.set("spark.sql.sources.maxPartitionBytes", "134217728") 

# COMMAND ----------

# MAGIC %run ../setup/configurations

# COMMAND ----------

# DBTITLE 1,Defining the schema
schema = StructType([StructField('address_1', StringType(), True), StructField('address_2', StringType(), True), StructField('address_3', StringType(), True), StructField('brewery_type', StringType(), True), StructField('city', StringType(), True), StructField('country', StringType(), True), StructField('id', StringType(), True), StructField('latitude', DoubleType(), True), StructField('longitude', DoubleType(), True), StructField('name', StringType(), True), StructField('phone', StringType(), True), StructField('postal_code', StringType(), True), StructField('state', StringType(), True), StructField('state_province', StringType(), True), StructField('street', StringType(), True), StructField('website_url', StringType(), True)])

# COMMAND ----------

# DBTITLE 1,Reading raw files from Blob Storage
raw_data = spark.read.json(bronze_path, schema=schema)

# COMMAND ----------

raw_data.schema

# COMMAND ----------

# DBTITLE 1,Writing to silver layer
raw_data.write.format("parquet").mode("overwrite").partitionBy("state").option("compression", "snappy").save(silver_path)

# COMMAND ----------

silver_df = spark.read.parquet(silver_path)