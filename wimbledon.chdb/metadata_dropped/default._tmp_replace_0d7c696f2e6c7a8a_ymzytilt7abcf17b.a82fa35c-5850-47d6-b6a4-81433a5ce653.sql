ATTACH TABLE _ UUID 'a82fa35c-5850-47d6-b6a4-81433a5ce653'
(
    `p1Name` Nullable(String),
    `p2Name` Nullable(String),
    `match` String,
    `event` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
