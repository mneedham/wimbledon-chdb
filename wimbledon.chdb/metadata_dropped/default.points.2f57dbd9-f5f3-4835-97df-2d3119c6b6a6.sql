ATTACH TABLE _ UUID '2f57dbd9-f5f3-4835-97df-2d3119c6b6a6'
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
