ATTACH TABLE _ UUID 'd02af9a4-603f-4745-b2fa-59b37a9c4d76'
(
    `p1Name` Nullable(String),
    `p2Name` Nullable(String),
    `match` String,
    `event` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
