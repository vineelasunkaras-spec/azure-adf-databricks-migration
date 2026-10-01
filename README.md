# Azure Data Migration — ADF + Databricks + ADLS Gen2 (Medallion)

Metadata-driven migration of on-premises **Oracle** and **Teradata** tables to **Azure Data Lake Storage Gen2** using **Azure Data Factory v2**, followed by **Azure Databricks** bronze → silver → gold processing.

## How it works
1. `adf/pl_metadata_driven_copy.json` — a **Lookup** reads a control table, **Filter** keeps enabled tables, **ForEach** runs a parallel **Copy** activity per table (full or incremental by watermark) into `bronze/` as Parquet.
2. A **Databricks Notebook** activity (`notebooks/bronze_to_silver.py`) standardizes types, deduplicates, and writes Delta tables to `silver/`.
3. `notebooks/silver_to_gold.py` builds aggregated, analytics-ready Delta tables in `gold/`.
4. The control table watermark is updated on success.

```
Oracle / Teradata ──(Self-hosted IR)──► ADF Copy ──► ADLS bronze (Parquet)
                                                         │ Databricks
                                                         ▼
                                               silver (Delta) ──► gold (Delta) ──► Power BI / Synapse
```

## Repo layout
| Path | Purpose |
|------|---------|
| `adf/` | ADF pipeline, linked service and dataset JSON definitions |
| `adf/control_table.sql` | Metadata control table DDL + sample rows |
| `notebooks/` | PySpark notebooks (Databricks source format) and shared helpers |
| `tests/` | Unit tests for helper logic |

## Tech
Azure Data Factory · Azure Databricks · ADLS Gen2 · Delta Lake · PySpark · Oracle · Teradata · Azure Key Vault
