ATTACH TABLE _ UUID '1d647cff-5451-470a-a603-5fbd52a4c7f5'
(
    `p1Name` Nullable(String),
    `p2Name` Nullable(String),
    `match` String,
    `event` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
