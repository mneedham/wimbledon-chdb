ATTACH TABLE _ UUID 'f0df3905-7dc4-4d7c-b96d-0756af695187'
(
    `json` JSON,
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
