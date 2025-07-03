ATTACH TABLE _ UUID '0e52503b-e95b-4bfc-9df2-3ea5dfc29f0e'
(
    `p1Name` Nullable(String),
    `p2Name` Nullable(String),
    `match` String,
    `event` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
