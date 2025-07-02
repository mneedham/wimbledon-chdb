ATTACH TABLE _ UUID 'ab5a7768-bb2e-4dfe-b21d-f1062b7074c4'
(
    `json` JSON,
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
