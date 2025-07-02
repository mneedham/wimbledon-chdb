CREATE FUNCTION pointsToWinOtherSetsBO5 AS (setScore, assumeWinSet) -> ((3 - (setScore + assumeWinSet)) * 24)
