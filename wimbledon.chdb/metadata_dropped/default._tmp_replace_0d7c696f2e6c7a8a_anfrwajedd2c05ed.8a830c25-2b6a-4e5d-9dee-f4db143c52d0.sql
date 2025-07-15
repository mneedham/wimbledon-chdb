ATTACH TABLE _ UUID '8a830c25-2b6a-4e5d-9dee-f4db143c52d0'
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
