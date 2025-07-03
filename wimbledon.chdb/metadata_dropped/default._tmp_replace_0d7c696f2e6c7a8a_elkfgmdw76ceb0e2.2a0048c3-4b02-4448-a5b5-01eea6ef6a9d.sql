ATTACH TABLE _ UUID '2a0048c3-4b02-4448-a5b5-01eea6ef6a9d'
(
    `json` JSON,
    `match` String
)
ENGINE = MergeTree
ORDER BY match
SETTINGS index_granularity = 8192
