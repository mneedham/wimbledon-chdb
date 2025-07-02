ATTACH TABLE _ UUID '080421c4-8956-474f-a0e3-b59f78534008'
(
    `json` JSON,
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
