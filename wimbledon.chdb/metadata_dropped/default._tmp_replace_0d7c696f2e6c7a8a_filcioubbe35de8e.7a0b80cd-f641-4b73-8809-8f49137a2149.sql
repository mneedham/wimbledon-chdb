ATTACH TABLE _ UUID '7a0b80cd-f641-4b73-8809-8f49137a2149'
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
