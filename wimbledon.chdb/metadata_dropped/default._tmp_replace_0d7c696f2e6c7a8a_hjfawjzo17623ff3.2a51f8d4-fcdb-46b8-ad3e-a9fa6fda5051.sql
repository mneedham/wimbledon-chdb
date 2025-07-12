ATTACH TABLE _ UUID '2a51f8d4-fcdb-46b8-ad3e-a9fa6fda5051'
(
    `p1Name` Nullable(String),
    `p2Name` Nullable(String),
    `match` String,
    `event` String,
    `roundName` Dynamic,
    `eventName` Dynamic,
    `courtName` Dynamic,
    `roundNameShort` Dynamic
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
