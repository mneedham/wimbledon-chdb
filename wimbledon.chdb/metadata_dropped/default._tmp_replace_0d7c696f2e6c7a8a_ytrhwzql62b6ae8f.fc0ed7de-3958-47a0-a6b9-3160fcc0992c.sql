ATTACH TABLE _ UUID 'fc0ed7de-3958-47a0-a6b9-3160fcc0992c'
(
    `p1Name` Nullable(String),
    `p2Name` Nullable(String),
    `match` String,
    `event` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
