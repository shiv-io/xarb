CREATE TABLE PUBLIC.cb_ticker (
    base text COLLATE pg_catalog."default",
    currency text COLLATE pg_catalog."default",
    amount DOUBLE PRECISION,
    created_at timestamp NOT NULL,
    TYPE text COLLATE pg_catalog."default",
    constraint cb_ticker_pkey primary key (created_at)
);
CREATE TABLE PUBLIC.fx (
    last_updated_at timestamp NOT NULL,
    usd bigint,
    cad DOUBLE PRECISION,
    inr DOUBLE PRECISION,
    constraint fx_pkey primary key (last_updated_at)
);
CREATE TABLE PUBLIC.wazirx_ticker (
    base_unit text COLLATE pg_catalog."default",
    quote_unit text COLLATE pg_catalog."default",
    low text COLLATE pg_catalog."default",
    high text COLLATE pg_catalog."default",
    last text COLLATE pg_catalog."default",
    TYPE text COLLATE pg_catalog."default",
    OPEN DOUBLE PRECISION,
    volume text COLLATE pg_catalog."default",
    sell text COLLATE pg_catalog."default",
    buy text COLLATE pg_catalog."default",
    AT timestamp,
    NAME text COLLATE pg_catalog."default"
);
-- CREATE
-- OR REPLACE VIEW PUBLIC.stg_cb_ticker AS
-- SELECT
--     cb_ticker.base,
--     cb_ticker.currency,
--     cb_ticker.amount,
--     cb_ticker.created_at,
--     cb_ticker.type,
--     TO_TIMESTAMP(
--         cb_ticker.created_at :: DOUBLE PRECISION
--     ) AS created_at_timestamp
-- FROM
--     cb_ticker;
-- CREATE
--     OR REPLACE VIEW PUBLIC.stg_fx AS
-- SELECT
--     fx.last_updated_at,
--     TO_TIMESTAMP(
--         fx.last_updated_at :: DOUBLE PRECISION
--     ) AS last_updated_timestamp,
--     fx.usd,
--     fx.cad,
--     fx.inr
-- FROM
--     fx;
-- CREATE
--     OR REPLACE VIEW PUBLIC.stg_price AS
-- SELECT
--     s.type,
--     s.name,
--     s.base_unit,
--     s.quote_unit,
--     s.low,
--     s.high,
--     s.last,
--     s.open,
--     s.volume,
--     s.sell,
--     s.buy,
--     s.at,
--     s.created_at,
--     f.usd,
--     f.cad,
--     f.inr
-- FROM
--     stg_ticker s
--     CROSS JOIN (
--         SELECT
--             stg_fx.last_updated_at,
--             stg_fx.last_updated_timestamp,
--             stg_fx.usd,
--             stg_fx.cad,
--             stg_fx.inr
--         FROM
--             stg_fx
--         ORDER BY
--             stg_fx.last_updated_at DESC
--         LIMIT
--             1
--     ) f
-- ORDER BY
--     s.created_at DESC;
-- CREATE
--     OR REPLACE VIEW PUBLIC.stg_wazirx_ticker AS
-- SELECT
--     ticker.type,
--     ticker.name,
--     ticker.base_unit,
--     ticker.quote_unit,
--     ticker.low :: DOUBLE PRECISION AS low,
--     ticker.high :: DOUBLE PRECISION AS high,
--     ticker.last :: DOUBLE PRECISION AS last,
--     ticker.open,
--     ticker.volume :: DOUBLE PRECISION AS volume,
--     ticker.sell :: DOUBLE PRECISION AS sell,
--     ticker.buy :: DOUBLE PRECISION AS buy,
--     ticker.at,
--     TO_TIMESTAMP(
--         ticker.at :: DOUBLE PRECISION
--     ) AS created_at
-- FROM
--     wazirx_ticker;
-- CREATE
--     OR REPLACE VIEW PUBLIC.last_arb AS
-- SELECT
--     s.type,
--     s.name,
--     s.base_unit,
--     s.quote_unit,
--     s.low,
--     s.high,
--     s.last,
--     s.open,
--     s.volume,
--     s.sell,
--     s.buy,
--     s.at,
--     s.created_at,
--     s.usd,
--     s.cad,
--     s.inr,
--     s.last / s.inr AS wazirx_btc_usd,
--     C.amount AS coinbase_btc_usd,
--     C.created_at AS coinbase_updated_at,
--     s.last / s.inr - C.amount AS arbitrage_value_usd
-- FROM
--     PUBLIC.stg_price s
--     CROSS JOIN (
--         SELECT
--             stg_cb_ticker.base,
--             stg_cb_ticker.currency,
--             stg_cb_ticker.amount,
--             stg_cb_ticker.created_at,
--             stg_cb_ticker.type,
--             stg_cb_ticker.created_at_timestamp
--         FROM
--             stg_cb_ticker
--         ORDER BY
--             stg_cb_ticker.created_at DESC
--         LIMIT
--             1
--     ) C
-- WHERE
--     s.base_unit = 'btc' :: text
-- ORDER BY
--     s.created_at DESC
-- LIMIT
--     1;
