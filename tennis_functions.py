def init_functions(sess):
    sess.query("""
    CREATE OR REPLACE FUNCTION pointsToWinGame AS (p1Score, p2Score) -> 
        multiIf(
            p1Score = '40' AND p2Score = 'AD', 3,
            p1Score = '40' AND p2Score = '40', 2,
            p1Score = '40' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 1,
            p1Score = '30' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 2,
            p1Score = '30' AND p2Score = '40', 3,
            p1Score = '15' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 3,
            p1Score = '15' AND p2Score = '40', 4,
            p1Score = '0' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 4,
            p1Score = '0' AND p2Score = '40', 5,
            p1Score = 'AD', 1,
            0
        );
    """)

    sess.query("""
    CREATE OR REPLACE FUNCTION pointsToWinTiebreak AS (p1Score, p2Score) -> 
        if(
            p2Score <= 5, (7 - p1Score),
            (p2Score + 2) - p1Score
        );
    """)

    sess.query("""
    CREATE OR REPLACE FUNCTION pointsToWinMatchTiebreak AS (p1Score, p2Score) -> 
        if(
            p2Score <= 8, (10 - p1Score),
            (p2Score + 2) - p1Score
        );
    """)

    sess.query("""
    CREATE OR REPLACE FUNCTION pointsToWinSet AS (p1Score, p2Score, assumeWinNextGame) -> 
        multiIf(
            p2Score = 5, (7 - (p1Score+assumeWinNextGame)) * 4,
            p1Score+assumeWinNextGame = 7 AND p2Score = 6, 0,
            p2Score = 6, ((6 - (p1Score+assumeWinNextGame)) * 4) + 7,
            p1Score+assumeWinNextGame = 7, 0,
            p1Score+assumeWinNextGame = 6 AND p2Score < 5, 0,
            (6 - (p1Score+assumeWinNextGame)) * 4
        );
    """)

    sess.query("""
    CREATE OR REPLACE FUNCTION pointsToWinFinalSet AS (p1Score, p2Score, assumeWinNextGame) -> 
        multiIf(
            p2Score = 5, (7 - (p1Score+assumeWinNextGame)) * 4,
            p1Score+assumeWinNextGame = 7 AND p2Score = 6, 0,
            p2Score = 6, ((6 - (p1Score+assumeWinNextGame)) * 4) + 10,
            p1Score+assumeWinNextGame = 7, 0,
            p1Score+assumeWinNextGame = 6 AND p2Score < 5, 0,
            (6 - (p1Score+assumeWinNextGame)) * 4
        );
    """)

    sess.query("""
    CREATE OR REPLACE FUNCTION pointsToWinOtherSetsBO5 AS (setScore, assumeWinSet) -> (3 - (setScore+assumeWinSet)) * 24;
    """)

    sess.query("""
    CREATE OR REPLACE FUNCTION pointsToWinOtherSetsBO3 AS (setScore, assumeWinSet) -> (2 - (setScore+assumeWinSet)) * 24;
    """)


    sess.query("""
    CREATE OR REPLACE FUNCTION pointsToWinMatch AS (bestOf5, MatchWinner, GameWinner, SetWinner, whoAmI, mySetScore, theirSetScore, myGameScore, theirGameScore, myPointScore, theirPointScore) -> 
        multiIf(
        MatchWinner = whoAmI, 0,
        MatchWinner = '0',
        if(bestOf5, pointsToWinOtherSetsBO5(mySetScore::UInt32, NOT(SetWinner <> '0')), pointsToWinOtherSetsBO3(mySetScore::UInt32, NOT(SetWinner <> '0'))) + 
        multiIf(
        SetWinner <> '0', 0, 
        myGameScore = '6' AND theirGameScore='6' AND ((mySetScore = '2' AND theirSetScore='2' AND bestOf5) OR (mySetScore = '1' AND theirSetScore='1' AND NOT bestOf5)), 
        pointsToWinFinalSet(myGameScore::UInt32, theirGameScore::UInt32, NOT(GameWinner <> '0' OR SetWinner <> '0')),
        pointsToWinSet(myGameScore::UInt32, theirGameScore::UInt32, NOT(MatchWinner <> '0' OR SetWinner <> '0' OR GameWinner <> '0'))
        ) + 
        multiIf(
        GameWinner <> '0', 0, 
        myGameScore = '6' AND theirGameScore='6' AND ((mySetScore = '2' AND theirSetScore='2' AND bestOf5) OR (mySetScore = '1' AND theirSetScore='1' AND NOT bestOf5)), 
        pointsToWinMatchTiebreak(myPointScore::UInt32, theirPointScore::UInt32), 
        myGameScore = '6' AND theirGameScore='6', pointsToWinTiebreak(myPointScore::UInt32, theirPointScore::UInt32), 
        pointsToWinGame(myPointScore, theirPointScore)
        ),
        if(bestOf5, 72, 48)
        );
    """)