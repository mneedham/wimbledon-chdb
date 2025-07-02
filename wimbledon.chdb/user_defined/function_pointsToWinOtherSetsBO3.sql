CREATE FUNCTION pointsToWinOtherSetsBO3 AS (setScore, assumeWinSet) -> ((2 - (setScore + assumeWinSet)) * 24)
