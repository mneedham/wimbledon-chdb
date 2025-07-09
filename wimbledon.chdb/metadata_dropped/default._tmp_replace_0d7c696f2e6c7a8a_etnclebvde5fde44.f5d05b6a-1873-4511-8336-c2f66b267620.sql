ATTACH TABLE _ UUID 'f5d05b6a-1873-4511-8336-c2f66b267620'
(
    `p1Name` Nullable(String),
    `p2Name` Nullable(String),
    `match` String,
    `event` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
