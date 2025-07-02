ATTACH TABLE _ UUID '123c0fee-c318-45b2-95a8-e97fcf3bea62'
(
    `json` JSON,
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
