ATTACH TABLE _ UUID '84c0c51f-7b65-482b-a0ca-a978a2e301e2'
(
    `json` JSON,
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
