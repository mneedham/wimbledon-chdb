ATTACH TABLE _ UUID '460f3a7d-22c3-45ba-b445-df2c3fe85cc2'
(
    `p1Name` Nullable(String),
    `p2Name` Nullable(String),
    `match` String,
    `event` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
