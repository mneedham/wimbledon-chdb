CREATE FUNCTION pointsToWinMatchTiebreak AS (p1Score, p2Score) -> if(p2Score <= 8, 10 - p1Score, (p2Score + 2) - p1Score)
