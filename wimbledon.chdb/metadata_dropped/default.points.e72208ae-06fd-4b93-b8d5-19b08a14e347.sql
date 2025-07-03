ATTACH TABLE _ UUID 'e72208ae-06fd-4b93-b8d5-19b08a14e347'
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
