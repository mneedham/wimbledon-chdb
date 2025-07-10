ATTACH TABLE _ UUID 'e8ad2152-75c3-45a2-bf43-0dc7f25c652a'
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
