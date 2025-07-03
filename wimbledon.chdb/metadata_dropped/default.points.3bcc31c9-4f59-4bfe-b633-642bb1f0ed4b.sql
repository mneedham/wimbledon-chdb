ATTACH TABLE _ UUID '3bcc31c9-4f59-4bfe-b633-642bb1f0ed4b'
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
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
