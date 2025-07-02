CREATE FUNCTION pointsToWinOtherSets AS (setScore, assumeWinSet) -> ((3 - (setScore + assumeWinSet)) * 24)
