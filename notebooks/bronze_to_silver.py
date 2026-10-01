# Databricks notebook source
# MAGIC %md
# MAGIC ## Bronze → Silver
# MAGIC Standardize column names, dedupe by primary key, add audit columns, and MERGE into a Delta table.

# COMMAND ----------
dbutils.widgets.text("source_system", "ORACLE")
dbutils.widgets.text("table", "ORDERS")
dbutils.widgets.text("primary_keys", "ORDER_ID")

from delta.tables import DeltaTable
from pyspark.sql import Window
from pyspark.sql import functions as F

from notebooks.helpers import layer_path, parse_keys, to_snake_case

src = dbutils.widgets.get("source_system")
table = dbutils.widgets.get("table")
keys = parse_keys(dbutils.widgets.get("primary_keys"))

# COMMAND ----------
bronze = spark.read.parquet(layer_path("bronze", src, table))
df = bronze.toDF(*[to_snake_case(c) for c in bronze.columns])
df = (
    df.withColumn("_ingested_at", F.current_timestamp())
      .withColumn("_source_system", F.lit(src))
      .withColumn("_row_hash", F.sha2(F.concat_ws("||", *[F.col(c).cast("string") for c in df.columns]), 256))
)
order_col = next((c for c in df.columns if c in ("last_update_dt", "posting_ts", "updated_at")), "_ingested_at")
df = df.withColumn("_rn", F.row_number().over(Window.partitionBy(*keys).orderBy(F.col(order_col).desc()))) \
       .filter("_rn = 1").drop("_rn")

# COMMAND ----------
target = layer_path("silver", src, table)
if DeltaTable.isDeltaTable(spark, target):
    cond = " AND ".join(f"t.{k} = s.{k}" for k in keys)
    (DeltaTable.forPath(spark, target).alias("t")
        .merge(df.alias("s"), cond)
        .whenMatchedUpdateAll(condition="t._row_hash <> s._row_hash")
        .whenNotMatchedInsertAll()
        .execute())
else:
    df.write.format("delta").option("delta.autoOptimize.optimizeWrite", "true").save(target)

dbutils.notebook.exit(str(df.count()))
