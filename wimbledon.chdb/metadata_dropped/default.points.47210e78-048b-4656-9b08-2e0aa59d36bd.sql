ATTACH TABLE _ UUID '47210e78-048b-4656-9b08-2e0aa59d36bd'
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
