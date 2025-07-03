ATTACH TABLE _ UUID 'bb6f8587-cd60-4655-8e81-2690c3773e79'
(
    `MatchWinner` String,
    `SetWinner` String,
    `GameWinner` String,
    `P1SetsWon` String,
    `P2SetsWon` String,
    `P1GamesWon` String,
    `P2GamesWon` String,
    `P1Score` String,
    `P2Score` String,
    `ElapsedTime` String,
    `PointNumber` String,
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
