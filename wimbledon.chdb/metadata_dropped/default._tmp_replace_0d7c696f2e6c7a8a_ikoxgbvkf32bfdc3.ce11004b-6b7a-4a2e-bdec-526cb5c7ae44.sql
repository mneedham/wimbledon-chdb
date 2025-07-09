ATTACH TABLE _ UUID 'ce11004b-6b7a-4a2e-bdec-526cb5c7ae44'
(
    `p1Name` Nullable(String),
    `p2Name` Nullable(String),
    `match` String,
    `event` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
