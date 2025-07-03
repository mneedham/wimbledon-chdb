ATTACH TABLE _ UUID 'a80e135a-68a3-4e29-b615-8b1b8e392758'
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
