ATTACH TABLE _ UUID '1f9f5b8b-0b84-4418-a30a-2e31bfcbc0fb'
(
    `p1Name` Nullable(String),
    `p2Name` Nullable(String),
    `match` String,
    `event` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
