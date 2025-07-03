ATTACH TABLE _ UUID '076fabed-9f24-4792-af0b-6b4cd1bc758e'
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
