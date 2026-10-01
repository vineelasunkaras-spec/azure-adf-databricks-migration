CREATE TABLE etl.migration_control (
    table_id         INT IDENTITY PRIMARY KEY,
    source_system    VARCHAR(20)  NOT NULL,   -- ORACLE | TERADATA
    source_schema    VARCHAR(128) NOT NULL,
    source_table     VARCHAR(128) NOT NULL,
    load_type        VARCHAR(12)  NOT NULL,   -- FULL | INCREMENTAL
    watermark_column VARCHAR(128) NULL,
    last_watermark   DATETIME2    NULL,
    primary_keys     VARCHAR(400) NOT NULL,
    is_enabled       BIT          NOT NULL DEFAULT 1
);

INSERT INTO etl.migration_control (source_system, source_schema, source_table, load_type, watermark_column, last_watermark, primary_keys)
VALUES ('ORACLE',   'SALES',  'ORDERS',     'INCREMENTAL', 'LAST_UPDATE_DT', '1900-01-01', 'ORDER_ID'),
       ('ORACLE',   'SALES',  'CUSTOMERS',  'FULL',        NULL,             NULL,         'CUSTOMER_ID'),
       ('TERADATA', 'FIN_DB', 'GL_ENTRIES', 'INCREMENTAL', 'POSTING_TS',     '1900-01-01', 'ENTRY_ID,LINE_NO');
