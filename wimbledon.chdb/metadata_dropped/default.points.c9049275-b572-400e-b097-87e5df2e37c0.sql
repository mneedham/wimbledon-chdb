ATTACH TABLE _ UUID 'c9049275-b572-400e-b097-87e5df2e37c0'
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
