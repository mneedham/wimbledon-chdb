ATTACH TABLE _ UUID '5ef151d1-2c74-4b19-9063-28a619c6814f'
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
