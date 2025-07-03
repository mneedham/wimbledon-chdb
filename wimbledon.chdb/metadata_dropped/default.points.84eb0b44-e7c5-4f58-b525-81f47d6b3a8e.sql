ATTACH TABLE _ UUID '84eb0b44-e7c5-4f58-b525-81f47d6b3a8e'
(
    `MatchWinner` String,
    `SetWinner` String,
    `GameWinner` String,
    `p1` Tuple(setsWon String, gamesWon String, score String),
    `p2` Tuple(setsWon String, gamesWon String, score String),
    `ElapsedTime` String,
    `PointNumber` String,
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
