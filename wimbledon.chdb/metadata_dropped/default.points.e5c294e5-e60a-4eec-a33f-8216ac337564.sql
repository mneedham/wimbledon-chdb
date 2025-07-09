ATTACH TABLE _ UUID 'e5c294e5-e60a-4eec-a33f-8216ac337564'
(
    `MatchWinner` String,
    `SetWinner` String,
    `GameWinner` String,
    `p1` Tuple(setsWon UInt8, gamesWon UInt8, score String),
    `p2` Tuple(setsWon UInt8, gamesWon UInt8, score String),
    `ElapsedTime` String,
    `PointNumber` UInt16,
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
