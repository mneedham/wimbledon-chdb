CREATE FUNCTION pointsToWinTiebreak AS (p1Score, p2Score) -> if(p2Score <= 5, 7 - p1Score, (p2Score + 2) - p1Score)
