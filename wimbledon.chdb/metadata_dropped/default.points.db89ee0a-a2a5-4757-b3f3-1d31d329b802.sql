ATTACH TABLE _ UUID 'db89ee0a-a2a5-4757-b3f3-1d31d329b802'
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
