ATTACH TABLE _ UUID '930cb433-df04-49c3-a39d-7b6c1b8c41a4'
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
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
