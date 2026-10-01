# Databricks notebook source
# MAGIC %md
# MAGIC ## Silver → Gold: daily sales by customer

# COMMAND ----------
from pyspark.sql import functions as F

from notebooks.helpers import layer_path

orders = spark.read.format("delta").load(layer_path("silver", "oracle", "orders"))
customers = spark.read.format("delta").load(layer_path("silver", "oracle", "customers"))

gold = (
    orders.join(customers, "customer_id", "left")
    .groupBy(F.to_date("order_date").alias("order_date"), "customer_id", "region")
    .agg(F.countDistinct("order_id").alias("orders"), F.sum("order_amount").alias("revenue"))
)

(gold.write.format("delta").mode("overwrite")
    .partitionBy("order_date")
    .option("overwriteSchema", "true")
    .save(layer_path("gold", "sales", "daily_customer_sales")))

spark.sql(f"OPTIMIZE delta.`{layer_path('gold', 'sales', 'daily_customer_sales')}` ZORDER BY (customer_id)")
